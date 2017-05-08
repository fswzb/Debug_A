# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 11:00:36 2017

@author: Mike
"""

import tushare as ts
from datetime import datetime,date,time,timedelta
import time as t

import conf

# 从conf.py文件中导入相关参数
code = conf.codes[0]
contacts = conf.contacts
mode = conf.modes['level_A']
bot = conf.QQ_login()


def get_ticks(code):
    '''获取今天的历史分笔数据'''
    ticks = ts.get_today_ticks(code,retry_count=10)
    ticks.time = ticks.time.apply(lambda x:datetime.strptime(x,'%H:%M:%S'))
    ticks.sort_values(by='time',inplace=True)
    return ticks

def m_change(ticks,code):
    '''监控涨跌幅（5分钟、10分钟、累计）
    
    parameter
    ————————————————
    ticks  今日的历史分笔数据
    '''
    # 获取开盘价
    op = ts.get_realtime_quotes(code).loc[0,'open']
    op = float(op)
    # 计算累计涨跌幅
    max_today = ticks.price.max()
    min_today = ticks.price.min()
    c_today = (max_today - min_today)/op
    # 计算10分钟涨跌幅
    t0 = ticks.iloc[-1].time
    delta_10 = timedelta(minutes=10)
    t10 = t0 - delta_10
    ticks_10 = ticks[ticks.time > t10 ]



