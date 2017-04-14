# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 17:16:31 2017

@author: Mike
"""

import requests

 
#用户名是登录ihuyi.com账号名（例如：cf_demo123）
account  = "C21684649"
#密码 查看密码请登录用户中心->验证码、通知短信->帐户及签名设置->APIKEY
password = "de8c32f40ab3e6f2cbbf352f631cf46f"
 
mobile = "18679426374"
text = "您的验证码是：121254。请不要把验证码泄露给其他人。".encode(encoding='utf-8')

url = 'http://106.ihuyi.com/webservice/sms.php?method=Submit'

params = {'account':'18679426374',
          'password':'de8c32f40ab3e6f2cbbf352f631cf46f',
          'mobile':'18679426374',
          'content':text}

x = requests.post(url,params)
