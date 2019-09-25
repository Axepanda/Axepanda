import json
import requests
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
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
        if category == 'athletics' and crunchies == 'new':
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
            data_list = self._getdata(score_obj, data_list, crunchies='new')

        elif category == 'athletics' and crunchies == 'brave':
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
            data_list = self._getdata(score_obj, data_list, crunchies='brave')

        elif category == "recreation":
            pass
        response.datalist = data_list
        response.msg = "Query successfully"
        return Response(response.get_data)

    def _getdata(self, score_obj, data_list, crunchies):
        for index, item in enumerate(score_obj):
            data = {}
            data["total"] = item.get("total")
            data["of user"] = item.get("user__username")
            data["rank"] = index + 1
            data["crunchies"] = crunchies
            data_list.append(data)
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
        phone = request.GET.get('phone', None)
        total = request.GET.get('total', None)
        crunchies = request.GET.get('crunchies', None)
        crunchies = self._get_crunchies(crunchies)
        result_phone = detect_phone(phone)
        if result_phone.get('status') == 200:
            user_obj = UserInfo.objects.filter(phone=phone).first()
            if user_obj:
                datalist = []
                score_obj = ScoreRecord.objects.filter(user_id=user_obj.id, total=total, crunchies=crunchies).values(
                    "first", "second",
                    "third", "fourth",
                    "fifth", "sixth",
                    "seventh", "eighth",
                    "ninth", "tenth", "crunchies")

                for item in score_obj:
                    datalist.append(item)
                response.datalist = datalist
                response.msg = "Query successfully"
            else:
                response.status = 401
                response.msg = "User doesn't exist"
        else:
            response.status = 402
            response.msg = "Phone number is wrong"
        return Response(response.get_data)

    def _get_crunchies(self, crunchies):
        if crunchies == "new":
            return 0
        elif crunchies == "brave":
            return 1
        elif crunchies == "master":
            return 2
        else:
            return 3

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
        gender = request.data.get('gender', None)
        country = request.data.get('country', None)
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
        print(phone,type(phone))
        user = UserInfo.objects.filter(username=openid).first()
        if user:
            UserInfo.objects.filter(username=openid).update(gender=gender, nationality=country,phone=phone)
            token = generate_token(user.id, openid)
        else:
            user_obj = UserInfo.objects.create(username=openid, gender=gender, nationality=country,phone=phone)
            token = generate_token(user_obj.id, openid)
        response.msg = "Login Ok!"
        response.token = token
        response.openid = openid
        return Response(response.get_data)
