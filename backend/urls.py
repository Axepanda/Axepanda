#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Wwl

from django.urls import path
from backend import views

urlpatterns = [
    path('bdlogin/', views.BDLogin.as_view()),
    path('upload/', views.UploadFile.as_view()),
    path('notice/', views.NoticeView.as_view()),
]