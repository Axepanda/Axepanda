from django.shortcuts import render,HttpResponse,redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from user.common import UserResponse,detect_phone
from user.models import UserInfo,ScoreRecord
from Axepanda import settings
import os,datetime

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
        crunchies = request.GET.get('crunchies', None)
        category = request.GET.get('category', None)
        type = request.GET.get('type', "total")
        data_list = []
        current_month = datetime.datetime.now().month
        if category == 'athletics' and crunchies == 'new':
            if type == "month":
                score_dict = ScoreRecord.objects.filter(category=0, crunchies=0,
                                                        created__month=current_month).order_by("-total").values(
                    "user__username", "total").distinct()[:50]
            elif type == "quarter":
                score_dict = ScoreRecord.objects.filter(category=0, crunchies=0).filter(
                    created__month__in=[current_month, current_month + 1, current_month + 2]).order_by("-total").values(
                    "user__username", "total").distinct()[:50]
            else:
                score_dict = ScoreRecord.objects.filter(category=0, crunchies=0).order_by("-total").values(
                    "user__username", "total").distinct()[:50]
            data_list = self._getdata(score_dict, data_list,crunchies='new')

        elif category == 'athletics' and crunchies == 'brave':
            if type == "month":
                score_instance_list = ScoreRecord.objects.filter(category=0, crunchies=1,
                                                                 created__month=current_month).order_by(
                    "-total").values("user__username", "total").distinct()[:50]
            elif type == 'quarter':
                score_instance_list = ScoreRecord.objects.filter(category=0, crunchies=1).filter(
                    created__month__in=[current_month, current_month + 1, current_month + 2]).order_by("-total").values(
                    "user__username", "total").distinct()[:50]
            else:
                score_instance_list = ScoreRecord.objects.filter(category=0, crunchies=1).order_by("-total").values(
                    "user__username", "total").distinct()[:50]
            data_list = self._getdata(score_instance_list, data_list,crunchies='brave')

        elif category == "recreation":
            pass
        response.datalist = data_list
        response.msg = "Query successfully"
        return Response(response.get_data)

    def _getdata(self, score_dict, data_list,crunchies):
        for index, item in enumerate(score_dict):
            data = {}
            data["total"] = item.get("total")
            data["of user"] = item.get("user__username")
            data["rank"] = index + 1
            data["crunchies"] = crunchies
            data_list.append(data)
        return data_list

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
        total = request.GET.get('total',None)
        crunchies = request.GET.get('crunchies',None)
        result_phone = detect_phone(phone)
        if result_phone.get('status') == 200:
          user_obj = UserInfo.objects.filter(phone=phone).first()
          if user_obj:
              datalist = []
              score_dict = ScoreRecord.objects.filter(total=total,crunchies=crunchies).values("first","second","third","fourth",
                                                                                              "fifth","sixth","seventh","eighth",
                                                                                              "ninth","tenth")
              for k,v in score_dict.items():
                  data = {}
                  data[k] = v
                  datalist.append(data)
              response.datalist = datalist
          else:
              response.status = 401
              response.msg = "User doesn't exist"
        else:
            response.status = 402
            response.msg = "Phone number is wrong"
        return Response(response.get_data)
