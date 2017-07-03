# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 21:19:31 2017
存放重复使用的函数
@author: zb
"""
import functools
import time as t
import pandas as pd
import tushare as ts
from datetime import datetime

# 函数运行耗时计算装饰器
def time_cost(func):
    @functools.wraps(func)
    def wrapper(*args,**kw):
        start = t.time()
        # 调用被装饰的函数
        print('正在运行函数 %s() ...'%func.__name__)
        res = func(*args,**kw)
        end = t.time()
        print('函数%s()运行耗时：%.2f 秒'%(func.__name__,end-start))
        return res
    return wrapper

def xq_code_url(code):
    '''构成code在雪球的url'''
    s = code[0]
    if s == '6':
        return 'https://xueqiu.com/S/SH'+code
    elif s == '0':
        return 'https://xueqiu.com/S/SZ'+code

def open_url(url):
    '''使用默认浏览器打开url'''
    import webbrowser
    webbrowser.open(url)

def analyze_ticks(code,date=''):
    '''
    分析分笔数据，50万以上交易的买卖盘分布

    parameters
    ————————
        code  string   股票代码，如：600122
        date  string   日期，如：2017-03-16

    returns
    ————————
        trade_c  dict  各类交易盘大于50万的成交额
                       如：{'中性盘': 791856, '买盘': 40172912, '卖盘': 44908088}
    
    example
    ————————
        analyze_ticks('600122','2017-03-16')
        analyze_ticks("600122")
        
    '''
    today = datetime.now().strftime('%Y-%m-%d')
    try:
        # 获取code在date的分笔数据
        if date == "" or date == today:
            # 调用 ts.get_today_ticks 获取当日历史分笔
            datas = ts.get_today_ticks(code)
        else:
            # 调用 ts.get_tick_data 获取date日期的历史分笔
            datas = ts.get_tick_data(code,date)

        # 分析50万以上的买卖盘
        gt50 = datas[datas.amount>500000][['amount','type']]
        trade_c = gt50.groupby(['type']).apply(sum)['amount']
        trade_c = dict(trade_c)
        
        return trade_c 
        
    except:
        print('当前日期%s不是交易日'%date)
        
        
def csv_duplications(csv='realtime_quotes.csv'):
    '''csv数据去重'''
    import pandas as pd
    try:
        datas = pd.read_csv(csv,encoding='utf-8')
    except:
        datas = pd.read_csv(csv,encoding='gbk')
    datas_dul = datas.drop_duplicates() # 去重
    datas_dul.to_csv(csv,index=False)
    
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