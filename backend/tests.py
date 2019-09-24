from django.test import TestCase
# Create your tests here.
import base64
import json
from Crypto.Cipher import AES
from Axepanda import settings
import requests
cloudID="25_cKblmqmPidyaE0N2Th3tVpGpMdoN56NEiwnMrM5qTXswToa2ZNbXT4dsu5w"
code="0336BDqD0Cfbqk26Y3sD0OKEqD06BDq8"
encryptedData="06XL6PzvCI1Kd438LpvdPXdlVhknCHjZhpduLwnBIXAtY/RmDuqP6KonNsXhG5yNh9UIgX7gB6ElTBxGKqIa3PCEkOIcJpf6Kt75kVX1I+ARsG8xUfqTzgdMBzgFuHXH3oBuRi7OTcZOySCRNdzu19McqMwVroL7iW5Dg6nSp5C6zfOB4o+BtpNP/YDMhZd4GQWtNI9Yn3nCX1v1s8lp1Q=="
errMsg="getPhoneNumber:ok"
iv="u1mG5LH7hbdwTOVxpjObXQ=="
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
import base64
import json
from Crypto.Cipher import AES
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
