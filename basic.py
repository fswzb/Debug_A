# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 21:36:47 2017

@author: Mike
"""

import tushare as ts
import pandas as pd
from functions import time_cost
from datetime import datetime,date,time,timedelta

@time_cost
def update_all_codes():
    '''
    更新A股中所有股票代码
    '''
    all_ = ts.get_stock_basics()
    all_codes = pd.DataFrame(all_.name)
    all_codes['code'] = ['|'+str(ins) for ins in all_.index]
    all_codes.to_csv('all_codes_in_market_A.csv',index=False,
                     encoding = 'gbk')

@time_cost
def check_today_ticks(code,over=100000,to_csv=True):
    '''
    保存某只股票的当日交易明细
    parameters
    ----------------
        code  股票代码 如：600122
        over  成交金额在over数值以上
        to_csv  布尔变量，True表示将结果保存到csv文件中
    return
    ----------------
        datas  当日成交额在over数值以上的所有成交记录
    '''
    # 调用ts.get_today_ticks获取当日交易记录
    ticks = ts.get_today_ticks(code)
    datas = ticks[ticks.amount > over]
    # 保存结果
    if to_csv == True:
        res_csv = code + '_over_' + str(over)[0:2] + 'k.csv'
        datas.to_csv(res_csv, index=False)
    return datas


    

























