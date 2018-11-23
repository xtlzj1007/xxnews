# -*- coding: utf-8 -*-
import urllib.request  # 给url发送请求
import urllib.parse  # requests


class ZhenziSmsClient(object):
    def __init__(self, api_url, app_id, app_secret):
        self.api_url = api_url
        self.app_id = app_id
        self.app_secret = app_secret

    def send(self, number, message, messageId=''):
        data = {
            'appId': self.app_id,
            'appSecret': self.app_secret,
            'message': message,
            'number': number,
            'messageId': messageId
        }

        data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(self.api_url + '/sms/send.do', data=data)
        res_data = urllib.request.urlopen(req)
        res = res_data.read()
        res = res.decode('utf-8')
        return res

    def balance(self):
        data = {
            'appId': self.app_id,
            'appSecret': self.app_secret
        }
        data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(self.api_url + '/account/balance.do', data=data)
        res_data = urllib.request.urlopen(req)
        res = res_data.read()
        return res
