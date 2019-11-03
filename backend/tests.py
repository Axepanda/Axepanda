from django.test import TestCase
# Create your tests here.
import base64
import json
from Crypto.Cipher import AES
from Axepanda import settings
import requests
cloudID= "25_YHU9oySSdkcGRnDegX9dax1-cl9-KyKeXgw8K2g68XHUNX0vk9qrR2Cr_dA"
code= "043ZTk2i1JxZJv01hg0i1Wqs2i1ZTk25"
encryptedData= "6bQpj29qiwAF57tXo2Py/fTQ/zD3iLMz6Dj5Z6fGoKhxifTHzUnJvReCw7U/HUIVav+oxBzKTGI+z6KW6h3NnvWhFHQqJK9AAadTSiJcX4qZZ30Bp0uDDctrt4IsNDARO5vslIwjLEdwxyFPZ09udfBpY1qcryxnltVEfl/5c2vCQ/UdTGNBcQsXMKzSbtep5zG7MNUCnEX/fKXfKSggzQ=="
errMsg= "getPhoneNumber:ok"
iv= "UFmFCXRtdbEv9nhdm1yiDQ=="
#
url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code" \
            .format(settings.APP_ID, settings.APP_KEY, code)
r = requests.get(url)
res = json.loads(r.text)
print(res)
openid = res['openid'] if 'openid' in res else None
session_key = res['session_key'] if 'session_key' in res else None
print(session_key)
#
# class WXBizDataCrypt:
#     def __init__(self, appId, sessionKey):
#         self.appId = appId
#         self.sessionKey = sessionKey
#
#     def decrypt(self, encryptedData, iv):
#         # base64 decode
#         sessionKey = base64.b64decode(self.sessionKey)
#         encryptedData = base64.b64decode(encryptedData)
#         iv = base64.b64decode(iv)
#
#         cipher = AES.new(sessionKey, AES.MODE_CBC, iv)
#
#         decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))
#
#         if decrypted['watermark']['appid'] != self.appId:
#             raise Exception('Invalid Buffer')
#         return decrypted
#
#     def _unpad(self, s):
#         return s[:-ord(s[len(s)-1:])]
#
# pc = WXBizDataCrypt(settings.APP_ID, session_key)
# print(pc)
# res = pc.decrypt(encryptedData, iv)
# print(res)
# import base64
# import json
# from Crypto.Cipher import AES
class WXBizDataCrypt(object):
    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        '''
        对称解密使用的算法为 AES-128-CBC，数据采用PKCS#7填充。
        对称解密的目标密文为 Base64_Decode(encryptedData)。
        对称解密秘钥 aeskey = Base64_Decode(session_key), aeskey 是16字节。
        对称解密算法初始向量 为Base64_Decode(iv)，其中iv由数据接口返回。
        :param encryptedData:
        :param iv:
        :return:
        {
            "phoneNumber": "13580006666",
            "purePhoneNumber": "13580006666",
            "countryCode": "86",
            "watermark":
            {
                "appid":"APPID",
                "timestamp": TIMESTAMP
            }
        }
        '''
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        temp = cipher.decrypt(encryptedData)

        nexts = self._unpad(temp)
        # logger.info(nexts)

        # decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))

        decrypted = json.loads(nexts)

        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

pc = WXBizDataCrypt(settings.APP_ID, session_key)
print(pc)
res = pc.decrypt(encryptedData, iv)
print(res)
