from django.test import TestCase
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Axepanda.settings")
# import django
# django.setup()
#
# import pandas as pd
# file_path = '/Users/wuwanlei/Desktop/Axepanda/member socres.xlsx'
# # file_path = r"C:\Users\77922\Downloads\Axepanda-master\Axepanda\member socres.xlsx"
# def analysis_excel(path):
#     df = pd.read_excel(path)
#     df.fillna("",inplace=True)
#     df_list = []
#     for i in df.index.values:
#         df_line = df.loc[i,['姓名','性别','年龄','国籍','第1环','第2环','第3环','第4环','第5环',
#                             '第6环','第7环','第8环','第9环','第10环','总分','类别','榜单','录入时间',]].to_dict()
#         df_list.append(df_line)
#     return df_list
# print(analysis_excel(file_path))
#
# for item in analysis_excel(file_path):
#     username = item.get('姓名')
#     gender = item.get('性别')
#     age = item.get('年龄')
#     nationality = item.get('国籍')
#     category = item.get('类别')
#     crunchies = item.get('榜单')
#     created = item.get('录入时间').to_pydatetime()
#     first = item.get('第1环')
#     second = item.get('第2环')
#     third = item.get('第3环')
#     fourth = item.get('第4环')
#     fifth = item.get('第5环')
#     sixth = item.get('第6环')
#     seventh = item.get('第7环')
#     eighth = item.get('第8环')
#     ninth = item.get('第9环')
#     tenth = item.get('第10环')
#     total = item.get('总分')
#     print(username,gender,age,nationality,category,crunchies,created)
    # if username == 'panda008':
    #     from user.models import UserInfo,Score
    #     user_obj = UserInfo.objects.create(username=username,gender=gender,age=age,nationality=nationality,category=category,
    #                                   crunchies=crunchies,created=created)
    #     score_obj = Score.objects.create(total=total,sixth=sixth,user=user_obj)