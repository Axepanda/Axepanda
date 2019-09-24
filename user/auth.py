#!/usr/bin/env python
# -*- coding:utf-8 -*-
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from user.common import verify_token


class JSONWebTokenAuth(BaseAuthentication):
    def authenticate(self, request, *args, **kwargs):
        pack = request.headers.get('Authorization', None)
        if pack is None:
            raise AuthenticationFailed('You are not logged in yet, please login first')
        parts = pack.split()
        # Authorization Header value must be 'jwt <token_value>'
        if parts[0].lower() != 'jwt':
            raise AuthenticationFailed("Invalid Token")
        elif len(parts) == 1:
            raise AuthenticationFailed("Token missing")
        elif len(parts) > 2:
            raise AuthenticationFailed("Invalid Token")
        token = parts[1].lstrip('<').rsplit('>')[0]
        res = verify_token(token)
        if str(res).startswith('40'):
            raise AuthenticationFailed(str(res).split(',')[1])
        else:
            return res, token

    def authenticate_header(self, request):
        pass
