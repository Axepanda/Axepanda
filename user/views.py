import json
import requests
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.common import UserResponse, detect_phone, generate_token
from user.models import UserInfo, ScoreRecord
from Axepanda import settings
import os, datetime
import base64
import json
from Crypto.Cipher import AES


class IndexDetail(APIView):
    def get(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = UserResponse()
        crunchies = request.GET.get('crunchies', None)
        category = request.GET.get('category', None)
        type = request.GET.get('type', "total")
        data_list = []
        current_month = datetime.datetime.now().month
        if category == 'athletics' and crunchies == "0":
            if type == "month":
                score_obj = ScoreRecord.objects.filter(category=0, crunchies=0,
                                                       created__month=current_month).order_by("-total").values(
                    "user__username", "total").distinct()[:50]
            elif type == "quarter":
                score_obj = ScoreRecord.objects.filter(category=0, crunchies=0).filter(
                    created__month__in=[current_month, current_month + 1, current_month + 2]).order_by("-total").values(
                    "user__username", "total").distinct()[:50]
            else:
                score_obj = ScoreRecord.objects.filter(category=0, crunchies=0).order_by("-total").values(
                    "user__username", "total").distinct()[:50]
            data_list = self._getdata(score_obj, data_list, crunchies=crunchies)

        elif category == 'athletics' and crunchies == "1":
            if type == "month":
                score_obj = ScoreRecord.objects.filter(category=0, crunchies=1,
                                                       created__month=current_month).order_by(
                    "-total").values("user__username", "total").distinct()[:50]
            elif type == 'quarter':
                score_obj = ScoreRecord.objects.filter(category=0, crunchies=1).filter(
                    created__month__in=[current_month, current_month + 1, current_month + 2]).order_by("-total").values(
                    "user__username", "total").distinct()[:50]
            else:
                score_obj = ScoreRecord.objects.filter(category=0, crunchies=1).order_by("-total").values(
                    "user__username", "total").distinct()[:50]
            data_list = self._getdata(score_obj, data_list, crunchies=crunchies)

        elif category == 'athletics' and crunchies == "3":
            if type == "month":
                score_obj = ScoreRecord.objects.filter(category=0, crunchies=3,
                                                       created__month=current_month).order_by(
                    "-total").values("user__username", "total").distinct()[:50]
            elif type == 'quarter':
                score_obj = ScoreRecord.objects.filter(category=0, crunchies=3).filter(
                    created__month__in=[current_month, current_month + 1, current_month + 2]).order_by("-total").values(
                    "user__username", "total").distinct()[:50]
            else:
                score_obj = ScoreRecord.objects.filter(category=0, crunchies=3).order_by("-total").values(
                    "user__username", "total").distinct()[:50]
            data_list = self._getdata(score_obj, data_list, crunchies=crunchies)

        elif category == "recreation":
            pass
        response.datalist = data_list
        response.msg = "Query successfully"
        return Response(response.get_data)

    def _getdata(self, score_obj, data_list, crunchies):
        for index, item in enumerate(score_obj):
            data = {}
            total = item.get("total")
            of_user = item.get("user__username")
            avatar = item.get("user__avatar")
            rank = index + 1
            crunchies = crunchies
            openid = item.get("user__openid")
            # 找到每个人在不同榜单上的排名。并存当前排名
            obj = ScoreRecord.objects.filter(user__username=of_user,crunchies=int(crunchies),total=total).first()
            if obj:
                if (obj.rank == None) or (obj.rank > rank) :
                    obj.rank = rank
                    obj.save()
            data["total"] = total
            data["of_user"] = of_user
            data["avater"] = avatar
            data["rank"] = rank
            data["openid"] = openid
            data["crunchies"] = crunchies
            data_list.append(data)
        print(data_list)
        return data_list



class UserDetail(APIView):
    def get(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = UserResponse()
        openid = request.GET.get('openid', None)
        user_obj = UserInfo.objects.filter(openid=openid).first()
        if user_obj:
            datalist = []
            score_obj = ScoreRecord.objects.filter(user_id=user_obj.id).values(
                "first", "second",
                "third", "fourth",
                "fifth", "sixth",
                "seventh", "eighth",
                "ninth", "tenth", "crunchies","total","rank")

            for item in score_obj:
                data = self._data_process(item)
                if len(data) == 13 and data[-1] != None:
                    datalist.append(data)
            response.username = user_obj.username
            response.avatar = user_obj.avatar
            response.datalist = datalist
            response.msg = "Query successfully"
        else:
            response.status = 401
            response.msg = "User doesn't exist"
        return Response(response.get_data)

    def _data_process(self,item):
        score = []
        for i in item.values():
                score.append(i)
        return score


class WXBizDataCrypt:
    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))

        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')
        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]


class WechatLoginView(APIView):
    def post(self, request, *args, **kwargs):
        response = UserResponse()
        code = request.data.get('code', None)
        encryptedData = request.data.get('encryptedData', None)
        iv = request.data.get('iv', None)
        if not code:
            return Response({'message': 'lack code'}, status=status.HTTP_400_BAD_REQUEST)

        url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code" \
            .format(settings.APP_ID, settings.APP_KEY, code)
        r = requests.get(url)
        res = json.loads(r.text)
        openid = res['openid'] if 'openid' in res else None
        session_key = res['session_key'] if 'session_key' in res else None
        if not openid:
            return Response({'message': 'The call to WeChat failed'}, status=status.HTTP_400_BAD_REQUEST)
        pc = WXBizDataCrypt(settings.APP_ID, session_key)
        res = pc.decrypt(encryptedData, iv)
        print(res,type(res))
        phone = res.get('phoneNumber')
        print(phone)
        user = UserInfo.objects.filter(openid=openid).first()
        if user:
            UserInfo.objects.filter(username=openid).update(phone=phone)
            token = generate_token(user.id, openid)
            response.msg = "登录成功"
        else:
            user_obj = UserInfo.objects.create(openid=openid,phone=phone)
            token = generate_token(user_obj.id, openid)
            response.msg = "暂无排名,等待后台上传成绩"
        response.token = token
        response.phone = phone
        response.openid = openid
        response.phone = phone
        return Response(response.get_data)


class GetUserInfo(APIView):
    def post(self,request,*args,**kwargs):
        response = UserResponse()
        gender = request.data.get('gender', None)
        nationality = request.data.get('nationality', None)
        avatar = request.data.get('avatar', None)
        openid = request.data.get('openid', None)
        print(gender,nationality,avatar,openid)
        if not all([gender,nationality,avatar,openid]):
            return Response({"status":401,"msg":"数据不完整"})
        if openid:
            user_obj = UserInfo.objects.filter(openid=openid)
            if user_obj:
                UserInfo.objects.filter(openid=openid).update(gender=gender,nationality=nationality,avatar=avatar)
                response.msg = "传送信息成功"
            else:
                response.status = 402
                response.msg = "无效openid，没有对应的用户"
        else:
            response.status = 403
            response.msg = "openid 不存在"
        return Response(response.get_data)
