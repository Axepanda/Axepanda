#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Wwl
class UserResponse():
    def __init__(self):
        self.status = 200
        self.msg = None

    @property
    def get_data(self):
        return self.__dict__