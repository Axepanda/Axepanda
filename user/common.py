#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Wwl
import re
class UserResponse():
    def __init__(self):
        self.status = 200
        self.msg = None

    @property
    def get_data(self):
        return self.__dict__

def detect_phone(phone):
    """
    verify phone
    """
    if phone == None or phone == '':
        return {'status': 400, 'msg': "The value is Empty"}
    regexp = r'^1[35678]\d{9}$'
    if not re.match(regexp, phone):
        return {"status": 405, "msg": "The phone number is illegal"}
    return {"status": 200, "msg": "verify successfully"}