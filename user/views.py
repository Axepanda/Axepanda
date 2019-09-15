from django.shortcuts import render,HttpResponse,redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from user.common import UserResponse
from user.models import UserInfo,Score
from Axepanda import settings

def get_file(request,*args,**kwargs):
    uploadedFile = request.FILES.get('filename')
    return HttpResponse('上传ok')



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