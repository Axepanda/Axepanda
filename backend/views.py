from django.shortcuts import render,redirect,HttpResponse
from rest_framework.authentication import BaseAuthentication
from rest_framework.views import APIView,Response
from user.common import UserResponse
from user.views import UserInfo
from Axepanda import settings
import os
from backend.common import analysis_excel,read_data
from backend.models import ExcelFile,Notice
from user.auth import JSONWebTokenAuth

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
            if superuser_obj.password == password:
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
        file_size = file.size
        suffix = file_name.split('.')[1]
        if not self._detect_suffix(suffix):
            response.status = 402
            response.msg = "The file is not in the right format"
            return Response(response.get_data)
        else:
            # file_path = settings.MEDIA_ROOT + '\\' + file.name
            file_path = os.path.join(settings.MEDIA_ROOT,file_name)
            print(file_path)
            if os.path.exists(file_path):
                self._write_file(file_path, file)
                self._import_excel(file_path, response, file_name, file_size)
            else:
                self._write_file(file_path, file)
                self._import_excel(file_path, response, file_name, file_size)
            return Response(response.get_data)

    def _write_file(self, file_path, file):
        with open(file_path, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)

    def _detect_suffix(self, suffix):
        if not suffix:
            return False
        elif suffix.lower() == 'xlsx' or suffix.lower() == 'csv':
            return True
        else:
            return False

    def _import_excel(self, file_path, response, file_name, file_size):
        result = read_data(df_list=analysis_excel(file_path))
        if result.get("status") == 200:
            ExcelFile.objects.create(filename=file_name, size=file_size, path=file_path)
            response.msg = "Upload successfully"
        else:
            response.msg = result.get("msg")

class NoticeView(APIView):
    # authentication_classes = [JSONWebTokenAuth,]
    def get(self,request,*args,**kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = UserResponse()
        notice_obj = Notice.objects.order_by("-created").distinct()[:3]
        datalist = []
        for item in notice_obj:
            datalist.append(item.content)
        response.msg = "Query successfully"
        response.datalist = datalist
        return Response(response.get_data)

    def post(self,request,*args,**kwargs):
        response = UserResponse()
        content = request.data.get("content",None)
        if content:
            Notice.objects.create(content=content)
            response.msg = "Add notice successfully"
        else:
            response.status = 401
            response.msg = "Content is Null"
        return Response(response.get_data)
