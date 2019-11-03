#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Wwl
from datetime import datetime, timedelta
from Axepanda import settings
from user.models import UserInfo
import jwt
import time, re

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

def generate_token(id, username):
    """create json web token
    create token，Valid for 1 day
    token
    """
    # token Expiration time, default expires after one day
    exp = datetime.utcnow() + timedelta(days=settings.TOKEN_EXPIRED_TIME)

    payload = {
        'user_id': id,
        'username': username,
        'exp': exp,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')

def verify_token(token):
    """Check verification json web token
    Args:
        token(str): json web token
    Return:
        object:user
    Raise:
        InvalidTokenError
    """
    try :
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except Exception as e :
        return "%s,%s"%(404,str(e))

    if any(('username' not in payload, 'user_id' not in payload, 'exp' not in payload)):
        return "403,invalid token"

    user_id = payload.get('user_id')

    user = UserInfo.objects.filter(id=user_id).first()

    if user is None:
        return "402,user not exist"
    return user