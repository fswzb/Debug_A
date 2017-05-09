# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 21:21:27 2017

@author: Mike
"""

import tushare as ts
from datetime import datetime,timedelta

# 从conf.py中导入相关参数
import conf
bot = conf.bot
contacts = conf.contacts


def notifier(bot,contacts,sms):
    '''使用QQ发送预警消息'''
    for contact in contacts:
        con = bot.List('buddy',contact)
        bot.SendTo(con[0],sms)
        

def get_ticks(code):
    '''获取今天的历史分笔数据,每次只能输入一只股票'''
    assert type(code) == str, ('get_ticks(code): code为单只股票代码，且必须是str')
    ticks = ts.get_today_ticks(code,retry_count=10)
    ticks.time = ticks.time.apply(lambda x:datetime.strptime(x,'%H:%M:%S'))
    ticks['code'] = code
    ticks.sort_values(by='time',inplace=True)
    return ticks



def m_change(ticks,mode_level='level_A'):
    '''监控波动（5分钟、10分钟、累计）
    
    parameter
    --------------------------------------
    ticks  今日的历史分笔数据  pd.DataFrame
    mode_level 监控模式，详见conf.py
    
    example
    --------------------------------------
    import monitor as m
        
    code = '600122'
    ticks = m.get_ticks(code)
    m.m_change(ticks,mode_level='level_C')
    
    '''
    # 获取开盘价、当日累计成交、换手
    code_ = ticks.code.unique()[0]
    assert type(code_) == str, ('code_为单只股票代码，且必须是str')
    data = ts.get_realtime_quotes(code_)
    op = float(data.loc[0,'open'])
    today_amount  = data.loc[0,'amount'].split('.')[0]
    
    # 计算今日累计波动
    max_today = ticks.price.max()
    min_today = ticks.price.min()
    c_today = (max_today - min_today)/op
    
    # 计算10分钟波动
    t0 = ticks.iloc[-1].time
    delta_10 = timedelta(minutes=10)
    t10 = t0 - delta_10
    ticks_10 = ticks[ticks.time > t10 ]
    max_in_10min = ticks_10.price.max()
    min_in_10min = ticks_10.price.min()
    c_10min = (max_in_10min - min_in_10min)/op
    
    # 计算5分钟波动
    delta_5 = timedelta(minutes=5)
    t5 = t0 - delta_5
    ticks_5 = ticks[ticks.time > t5 ]
    max_in_5min = ticks_5.price.max()
    min_in_5min = ticks_5.price.min()
    c_5min = (max_in_5min - min_in_5min)/op
    
    # 从conf获得监控参数
    mode = conf.modes[mode_level]
    
    # 构造预警消息
    sms1 = '{0}\n{1}\n全天波动：{2}%\n10分钟波动：{3}%\n5分钟波动{4}%' \
            .format(str(datetime.now()).split('.')[0],code_,
                    str(c_today*100)[0:5],
                    round(c_10min,4)*100,
                    round(c_5min,4)*100,)
    sms2 = '\n今日累计成交量：%s'%today_amount
    sms = sms1+sms2  
                  
    # 判断是否需要进行预警
    if c_today > mode['change_in_today']:
        send_sms = True
    elif c_5min > mode['change_in_5min']:
        send_sms = True
    elif c_10min > mode['change_in_10min']:
        send_sms = True
    elif datetime.now().minute%mode['inform_interval'] == 0:
        send_sms = True
    else:
        send_sms = False
    
    while send_sms:
        # 调用notifier发送预警消息
        notifier(bot,contacts,sms)
        send_sms = False


        
def m_big(ticks,mode_level='level_A'):
    '''监控大单
    
    parameter
    -----------------------------------------
    ticks  今日的历史分笔数据  pd.DataFrame
    mode_level 监控模式，详见conf.py
    -----------------------------------------
    import monitor as m
        
    code = '600122'
    ticks = m.get_ticks(code)
    m.m_change(ticks,mode_level='level_C')    
    
    '''
    # 从conf获得监控参数
    mode = conf.modes[mode_level]
    
    # 获取开盘价、当日累计成交、换手
    code_ = ticks.code.unique()[0]
    assert type(code_) == str, ('code_为单只股票代码，且必须是str')
    data = ts.get_realtime_quotes(code_)
    today_amount  = float(data.loc[0,'amount'].split('.')[0])
    
    # 计算今日累计大单
    big_ticks = ticks[ticks.amount > mode['over'][0]]
    cumsum_big = sum(big_ticks.amount)
    big_rate = cumsum_big/today_amount   # 今日大单成交占比
    
    # 计算10分钟大单数量
    t0 = ticks.iloc[-1].time
    delta_10 = timedelta(minutes=10)
    t10 = t0 - delta_10
    ticks_10 = big_ticks[big_ticks.time > t10 ]
    bm_10min = len(ticks_10)
    
    # 计算5分钟大单数量
    delta_5 = timedelta(minutes=5)
    t5 = t0 - delta_5
    ticks_5 = big_ticks[big_ticks.time > t5 ]
    bm_5min = len(ticks_5)
    
    # 构造预警消息
    sms1 = '{0}\n{1}\n今日大单累计成交 {2},占比 {3}。\n最近几分钟，大单密集，请注意！' \
            .format(str(datetime.now()).split('.')[0],code_,cumsum_big,big_rate)
    sms2 = '\n今日累计成交量：%s'%str(today_amount)
    sms = sms1 + sms2
    
    # 判断是否需要进行预警
    if bm_10min > mode['big_in_10min']:
        send_sms = True
    elif bm_5min > mode['big_in_5min']:
        send_sms = True
    elif datetime.now().minute%mode['inform_interval'] == 0:
        send_sms = True
    else:
        send_sms = False
    
    while send_sms:
        # 调用notifier发送预警消息
        notifier(bot,contacts,sms)
        send_sms = False    
    
    
