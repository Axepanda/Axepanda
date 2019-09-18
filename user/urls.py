#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Wwl
from django.urls import path
from user import views

urlpatterns = [
    path('code/', views.WXLogin.as_view()),
    path('index/', views.IndexDetail.as_view()),
    path('personal/', views.UserDetail.as_view())
]