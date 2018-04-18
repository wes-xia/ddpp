#-*- coding: utf-8 -*-

import requests
import json
import tempfile
import os
import random
import copy
import time

class BID_BASE():

    BID_CAPACHA_URL = 'http://pmcx.alltobid.com/GPCarQuery.Web/Image/ValiCode?'
    BID_QUERY_URL = 'http://pmcx.alltobid.com/GPCarQuery.Web/Home/Query'
    HEADERS = {
                'cookie':'ASP.NET_SessionId={}',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-HK;q=0.6',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host':'pmcx.alltobid.com',
                'Origin':'http://pmcx.alltobid.com',
                'Proxy-Connection': 'keep-alive',
                'Referer':'http://pmcx.alltobid.com/gpcarquery.web/home/personal',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
                }

    def __init__(self):

        r = requests.get(self.BID_CAPACHA_URL)
        cookies = r.cookies
        for item in cookies:
            if item.name == 'ASP.NET_SessionId':
                #print(item.value)
                self.SESSION =  item.value
                self.HEADERS['cookie'].format(item.value)

    def get_code(self):

        r = requests.get(self.BID_CAPACHA_URL, headers=self.HEADERS, cookies={'ASP.NET_SessionId':'%s'%self.SESSION})
#         cookies = r.cookies
#         for item in cookies:
#             if item.name == 'ASP.NET_SessionId':
#                 print item.value
        return r.content

    def check_bid(self, tender, idcard):

        code = self.get_code()
        vaild_code = validate_code(code)
        payload = dict(idcard=idcard, number=tender, type=2, code=int(vaild_code))
        #print('params', idcard, tender, vaild_code)
        result = requests.post(self.BID_QUERY_URL, data=payload, headers=self.HEADERS, cookies={'ASP.NET_SessionId':'%s'%self.SESSION})
        #print('text', result.text)
        info = json.loads(result.text)
        if info.get('err', ''):
            return False, info['err']
        else:
            return True, info

def validate_code(capacha):

    temp = tempfile.mkstemp(suffix=".png")
    os.write(temp[0], capacha)
    api_post_url = "http://v1-http-api.jsdama.com/api.php?mod=php&act=upload"
    validatorURL = api_post_url
    api_username = "jeromeyang"
    api_password = "1qaz@WSX"
    api_post_url = "http://v1-http-api.jsdama.com/api.php?mod=php&act=upload"
    yzm_min = 0000
    yzm_max = 9999
    params = { "user_name"      : '%s' % api_username,
               "user_pw"        : "%s" % api_password ,
               "yzm_minlen"     : "%s" % yzm_min ,
               "yzm_maxlen"     : "%s" % yzm_max ,
               "yzmtype_mark"   : "%s" % '' ,
               "zztool_token"   : "%s" % '' ,
               "upload"         : capacha,
             }
    files = {"upload" : open(temp[1], "rb"),}
    r = requests.post(validatorURL,  data=params, files=files)
    #print open(temp[1])
    info=json.loads(r.text)
    #print ('validate_code', info)
    #print ('validate_code', info['data'])
    return info['data']['val']

def check_bid_vaild(idcard, phone):
    """
    :param idcard: 身份证
    :param phone: 手机号
    :return: 拍牌申请结果
    """
    img_url = 'https://chepai.alltobid.com/PreCheckInApi/ImgCode/GenerateVerificationImage?'
    login_url = 'https://chepai.alltobid.com/PreCheckInApi/account/login?'
    userinfo_url = "https://chepai.alltobid.com/PreCheckInApi/PreCheckIn/GetCurUserInfo?"

    s = requests.session()
    res = s.get(img_url, stream=True)
    code = validate_code(res.content)
    params = """{"LoginMobile":"%s","LoginCertID":"%s","LoginVerificationCode":"%s"}"""%(phone, idcard, code)
    post_data = dict(parameter=params)
    rs = s.post(login_url, data=post_data)
    rs = s.post(userinfo_url)
    info = json.loads(rs.text)
    if info.get('ErrorMessage', ''):
        return False, info['ErrorMessage']
    else:
        return True, {
             'name': info['ReturnData']['name'],
             'reg_date': info['ReturnData']['RegDateStr'],
             'title': info['ReturnData']['title'],
        }





