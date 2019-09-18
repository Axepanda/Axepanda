from django.shortcuts import render,redirect,HttpResponse
from rest_framework.views import APIView,Response
from user.common import UserResponse
from user.views import UserInfo
from Axepanda import settings
import os

class BDLogin(APIView):
    def post(self,request,*args,**kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
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


class UploadFile(APIView):
    def post(self,request,*args,**kwargs):
        """
        :param request: {“panda_file”:"FILE"}
        :param args: None
        :param kwargs: None
        :return:
        """
        response = UserResponse()
        file = request.FILES.get('panda_file', None)
        if file is None:
            response.status = 401
            response.msg = "There is no file"
            return Response(response.get_data)
        file_name = file.name
        suffix = file_name.split('.')[1]
        if not self._detect_suffix(suffix):
            response.status = 402
            response.msg = "The file is not in the right format"
            return Response(response.get_data)
        else:
            file_path = settings.MEDIA_ROOT + '\\' + file.name
            if os.path.exists(file_path):
                self._write_file(file_path,file)
            else:
                self._write_file(file_path,file)
            response.msg = "Upload successfully"
            return Response(response.get_data)

    def _write_file(self,file_path,file):
        with open(file_path, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)

    def _detect_suffix(self,suffix):
        if not suffix:
            return False
        elif suffix.lower() == 'xlsx' or suffix.lower() == 'csv':
            return True
        else:
            return False


class Notice(APIView):
    def get(self,request,*args,**kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = UserResponse()
        pass
    def post(self,request,*args,**kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = UserResponse()
        pass