# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 20:25:18 2017

@author: Mike
"""

import tushare as ts
from datetime import datetime,time
import time as t
import pandas as pd

codes = ['600122','600977','601611','002256','002631','601595']

csv = 'realtime_quotes.csv'
while time(9,30,0) <= datetime.now().time() <= time(15,0,0):
    while time(9,30,0) <= datetime.now().time() <= time(11,30,0) or \
          time(13,0,0) <= datetime.now().time() <= time(15,0,0) :
             print('正在获取数据...')
             quotes = ts.get_realtime_quotes(codes)
             quotes.to_csv(csv,encoding='gbk',index=False,mode='a') 
             t.sleep(3)

# 读入数据去重
datas = pd.read_csv(csv,encoding='gbk')
datas_ = datas.drop_duplicates()
datas_ = datas_[datas_.name != 'name']
datas_ = datas_.sort_values(by=['name','date','time'])
datas_.to_csv(csv,encoding='gbk',index=False)
