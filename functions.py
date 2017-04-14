# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 21:19:31 2017
存放重复使用的函数
@author: Mike
"""
import functools
import time as t
import tushare as ts
from datetime import datetime,time,timedelta

# 自定义一个函数运行耗时计算装饰器
def time_cost(func):
    @functools.wraps(func)
    def wrapper(*args,**kw):
        start = t.time()
        # 调用被装饰的函数
        print('正在运行函数 %s() ...'%func.__name__)
        func(*args,**kw)
        end = t.time()
        print('函数%s()运行耗时：%.2f 秒'%(func.__name__,end-start))
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
        
        
def QQ_login(f_name):
    '''
    登录QQ机器人用于发送消息
    
    调用该函数之后会弹出一个二维码，使用用于发送消息的QQ扫码登录即可
    name 为 用于接收监控消息的qq备注名，即已登录QQ中的任一个好友
    '''
    from qqbot import QQBot
    bot = QQBot()
    bot.Login()  # 用需要登录的qq扫码
    con = bot.List('buddy',f_name)  # 获取好友列表
    sms = 'QQ机器人登录成功！'
    bot.SendTo(con[0],sms)
    return bot,con