from django.shortcuts import render,HttpResponse,redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from user.common import UserResponse,detect_phone
from user.models import UserInfo,Score
from Axepanda import settings
import os

class WXLogin(APIView):
    def post(self,request,*args,**kwargs):
        response = UserResponse()
        username = request.data.get("username",None)
        password = request.data.get("password",None)
        if username and password:
            superuser_obj = UserInfo.objects.filter(username=username).first()
            if superuser_obj.is_superuser == 1:
                response.msg = "login successfully"
            else:
                response.status = 401
                response.msg = "wrong password"
        else:
            response.status = 402
            response.msg = "The data is incomplete"
        return Response(response.get_data)


class IndexDetail(APIView):
    def get(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = UserResponse()
        list_name = request.GET.get('list_name',None)
        if list_name == 'brave':
            pass
        return Response(response.get_data)

class UserDetail(APIView):
    def get(self,request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = UserResponse()
        phone = request.GET.get('phone',None)
        result_phone = detect_phone(phone)
        if result_phone.get('status') == 200:
          user_obj = UserInfo.objects.filter(phone=phone).first()