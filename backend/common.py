#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Wwl
import pandas as pd
from user.models import UserInfo, ScoreRecord

def analysis_excel(path):
    df = pd.read_excel(path)
    df.fillna("", inplace=True)
    df_list = []
    for i in df.index.values:
        df_line = df.loc[i, ['姓名', '性别', '年龄', '国籍', '第1环', '第2环', '第3环', '第4环', '第5环',
                             '第6环', '第7环', '第8环', '第9环', '第10环', '总分', '类别', '榜单', '录入时间', ]].to_dict()
        df_list.append(df_line)
    return df_list

def read_data(df_list):
    for item in df_list:
        username = item.get('姓名')
        gender = item.get('性别')
        age = item.get('年龄')
        nationality = item.get('国籍')
        category = item.get('类别')
        if category == "竞技":
            category = 0
        else:
            category = 1
        crunchies = item.get('榜单')
        if crunchies == "新手榜":
            crunchies = 0
        elif crunchies == "勇士榜":
            crunchies = 1
        elif crunchies == "宗师榜":
            crunchies = 2
        else:
            crunchies = 3
        created = item.get('录入时间').to_pydatetime()
        first = item.get('第1环')
        second = item.get('第2环')
        third = item.get('第3环')
        fourth = item.get('第4环')
        fifth = item.get('第5环')
        sixth = item.get('第6环')
        seventh = item.get('第7环')
        eighth = item.get('第8环')
        ninth = item.get('第9环')
        tenth = item.get('第10环')
        total = item.get('总分')
        try:
            user = UserInfo.objects.filter(username=username).first()
            if user:
                ScoreRecord.objects.create(first=first,second=second,third=third,fourth=fourth,
                                           fifth=fifth,seventh=seventh,eighth=eighth,ninth=ninth,tenth=tenth,
                                        total=total,sixth=sixth,user_id=user.pk,crunchies=crunchies,category=category)
            else:
                user_obj = UserInfo.objects.create(username=username,gender=gender,age=age,nationality=nationality,created=created)
                ScoreRecord.objects.create(first=first,second=second,third=third,fourth=fourth,fifth=fifth,
                                                 seventh=seventh,eighth=eighth,ninth=ninth,tenth=tenth,
                                                 total=total,sixth=sixth,user_id=user_obj.id,crunchies=crunchies,category=category)
        except Exception as e :
            return {"status:":401,"msg":str(e)}
    return {"status":200,"msg":"import successfully"}