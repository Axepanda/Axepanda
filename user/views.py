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
from user.auth import JSONWebTokenAuth
import uuid,random

class IndexDetail(APIView):
    authentication_classes = [JSONWebTokenAuth,]
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
                    "user__phone", "total").distinct()[:50]
            else:
                score_obj = ScoreRecord.objects.filter(category=0, crunchies=0).order_by("-total").values(
                    "user__phone", "total").distinct()[:50]
            score_obj = self._distinct_score(score_obj)
            data_list = self._getdata(score_obj, data_list, crunchies=crunchies)

        elif category == 'athletics' and crunchies == "1":
            if type == "month":
                score_obj = ScoreRecord.objects.filter(category=0, crunchies=1,
                                                       created__month=current_month).order_by(
                    "-total").values("user__phone", "total").distinct()[:50]
            else:
                score_obj = ScoreRecord.objects.filter(category=0, crunchies=1).order_by("-total").values(
                    "user__phone", "total").distinct()[:50]
            score_obj = self._distinct_score(score_obj)
            data_list = self._getdata(score_obj, data_list, crunchies=crunchies)

        elif category == 'athletics' and crunchies == "3":
            if type == "month":
                score_obj = ScoreRecord.objects.filter(category=0, crunchies=3,
                                                       created__month=current_month).order_by(
                    "-total").values("user__phone", "total").distinct()[:50]
            else:
                score_obj = ScoreRecord.objects.filter(category=0, crunchies=3).order_by("-total").values(
                    "user__phone","total").distinct()[:50]
            score_obj = self._distinct_score(score_obj)
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
            phone = item.get("user__phone")
            user_obj = UserInfo.objects.filter(phone=phone).first()
            of_user = user_obj.username
            avatar = user_obj.avatar
            rank = index + 1
            crunchies = crunchies
            openid = user_obj.openid
            # 找到每个人在不同榜单上的排名。并存当前排名
            obj = ScoreRecord.objects.filter(user__openid=openid,crunchies=int(crunchies), total=total).first()
            if obj:
                if (obj.rank == None) or (obj.rank > rank):
                    obj.rank = rank
                    obj.save()
            data["total"] = total
            data["of_user"] = of_user
            data["avatar"] = avatar
            data["rank"] = rank
            data["openid"] = openid
            data["crunchies"] = crunchies
            data_list.append(data)
        return data_list

    def _distinct_score(self,score_obj):
        count_times = {}
        tmp = []
        for item in score_obj:
            count = count_times.get(item.get('user__phone'), 0) + 1
            count_times[item.get('user__phone')] = count
            if count <= 1:
                tmp.append(item)
        return tmp


class UserDetail(APIView):
    authentication_classes = [JSONWebTokenAuth,]
    def get(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = UserResponse()
        openid = request.GET.get('openid', None)
        crunchies = request.GET.get('crunchies', None)
        user_obj = UserInfo.objects.filter(openid=openid).first()
        if user_obj:
            datalist = []
            if crunchies:
                score_obj = ScoreRecord.objects.filter(user_id=user_obj.id, crunchies=crunchies).values(
                    "first", "second",
                    "third", "fourth",
                    "fifth", "sixth",
                    "seventh", "eighth",
                    "ninth", "tenth", "crunchies", "total", "rank")
            else:
                score_obj = ScoreRecord.objects.filter(user_id=user_obj.id).values(
                    "first", "second",
                    "third", "fourth",
                    "fifth", "sixth",
                    "seventh", "eighth",
                    "ninth", "tenth", "crunchies", "total", "rank")
            for item in score_obj:
                data = self._data_process(item)
                if data.get("rank") != None:
                    datalist.append(data)
            response.username = user_obj.username
            response.avatar = user_obj.avatar
            response.datalist = datalist
            response.msg = "Query successfully"
        else:
            response.status = 401
            response.msg = "User doesn't exist"
        return Response(response.get_data)

    def _data_process(self, item):
        score = {}
        tmp = []
        for k, v in item.items():
            if k not in ["total", "rank", "crunchies"]:
                tmp.append(v)
            else:
                score[k] = v
            score["gradelist"] = tmp
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
        return s[:-ord(s[len(s) - 1:])]


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
        phone = res.get('phoneNumber')
        print(phone)
        user = UserInfo.objects.filter(openid=openid).first()
        if user:
            UserInfo.objects.filter(openid=openid).update(phone=phone)
            token = generate_token(user.id, openid)
            response.msg = "登录成功"
        else:
            user_obj = UserInfo.objects.create(username=self._create_tmp_username(),openid=openid, phone=phone)
            token = generate_token(user_obj.id, openid)
            response.msg = "暂无排名,等待后台上传成绩"
        response.token = token
        response.phone = phone
        response.openid = openid
        return Response(response.get_data)

    def _create_tmp_username(self):
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, str(uuid.uuid1()) + str(random.random()))).replace('-','')[:12]


class GetUserInfo(APIView):
    def post(self, request, *args, **kwargs):
        response = UserResponse()
        gender = request.data.get('gender', None)
        nationality = request.data.get('nationality', None)
        avatar = request.data.get('avatar', None)
        openid = request.data.get('openid', None)
        nickname = request.data.get('nickName', None)
        if not all([gender, nationality, avatar, openid]):
            return Response({"status": 401, "msg": "数据不完整"})
        if openid:
            user_obj = UserInfo.objects.filter(openid=openid)
            if user_obj:
                try:
                    UserInfo.objects.filter(openid=openid).update(
                        nickname=nickname,gender=gender, nationality=nationality, avatar=avatar)
                    response.msg = "传送信息成功"
                except Exception as e :
                    response.status = 402
                    response.msg = str(e)
            else:
                response.status = 402
                response.msg = "无效openid，没有对应的用户"
        else:
            response.status = 403
            response.msg = "openid 不存在"
        return Response(response.get_data)
