#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Wwl
from django.urls import path
from user import views

urlpatterns = [
    path('wxlogin/', views.WechatLoginView.as_view()),
    path('index/', views.IndexDetail.as_view()),
    path('personal/', views.UserDetail.as_view())
]