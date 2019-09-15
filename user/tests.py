from django.test import TestCase

# Create your tests here.
# from openpyxl import Workbook,load_workbook
# from openpyxl.utils import get_column_letter
# from .models import UserInfo,Score
#
# def import_data(self,request,obj,change):
#     wb = load_workbook(filename='/Users/wuwanlei/Desktop/Axepanda/member socres.xlsx')
#     ws = wb.get_sheet_names()
#     ws = wb.get_sheet_by_name(ws[0])
#     headers = ['username','gender','age','nationality','first']
#
# import xlrd
# book = xlrd.open_workbook(filename='/Users/wuwanlei/Desktop/Axepanda/member socres.xlsx')
# sheet = book.sheet_by_name('Sheet1')
# ll = []
# for r in range(1,sheet.nrows):
#     data = {}
#     data['username'] = sheet.cell(r,0).value
#     data['gender'] = sheet.cell(r,1).value
#     data['age'] = sheet.cell(r,2).value
#     data['nation'] = sheet.cell(r,3).value
#     data['total_score'] = sheet.cell(r,14).value
#     data['category'] = sheet.cell(r,15).value
#     data['listt'] = sheet.cell(r,16).value
#     data['created'] = sheet.cell(r,17).value
#     ll.append(data)
# print(ll)


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Axepanda.settings")
import django
django.setup()

import pandas as pd
file_path = '/Users/wuwanlei/Desktop/Axepanda/member socres.xlsx'
def R(path):
    df = pd.read_excel(path)
    df.fillna("",inplace=True)
    df_list = []
    for i in df.index.values:
        df_line = df.loc[i,['姓名','性别','年龄','国籍','第1环','第2环','第3环','第4环','第5环',
                            '第6环','第7环','第8环','第9环','第10环','总分','类别','榜单','录入时间',]].to_dict()
        df_list.append(df_line)
    return df_list
#
# for item in func1(path):
#     username = item.get('姓名')
#     gender = item.get('性别')
#     age = item.get('年龄')
#     nation = item.get('国籍')
#     total = item.get('总分')
#     sixth = item.get('第7环')
#     print(username,gender,age,nation)
#     if username == 'panda008':
#         from user.models import UserInfo,Score
#         score_obj = Score.objects.create(total=total,sixth=sixth)
#         obj = UserInfo.objects.create(username=username,age=age,nationality=nation,score_id=score_obj.id)
