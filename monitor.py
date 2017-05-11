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
        
def m_price(code,high,low):
    '''监控股价'''
    assert type(code) == str,('code必须是单只股票代码，类型为str')
    assert high > low,('设定的最高价（high）必须大于最低价（low）！')
    cur = ts.get_realtime_quotes(code)
    name_ = cur.loc[0,'name']
    # 获取当前价格
    cp = float(cur.loc[0,'price'])
    assert type(high) == float,('high必须是float类型')
    if cp > high:
        # 构造预警消息
        sms = '{0}({1})当前价 {2}元，上穿设定的最高价 {3}元，请注意！' \
                .format(code,name_,cp,high,)
        # 调用notifier发送消息
        notifier(bot,contacts,sms)
    elif cp < low:
        # 构造预警消息
        sms = '{0}({1})当前价 {2}元，下穿设定的最低价 {3}元，请注意！' \
                .format(code,name_,cp,low,)
        # 调用notifier发送消息
        notifier(bot,contacts,sms)


def get_ticks(code):
    '''获取今天的历史分笔数据,每次只能输入一只股票'''
    assert type(code) == str, ('get_ticks(code): code为单只股票代码，且必须是str')
    ticks = ts.get_today_ticks(code,retry_count=18)
    ticks.time = ticks.time.apply(lambda x:datetime.strptime(x,'%H:%M:%S'))
    ticks['code'] = code
    ticks.sort_values(by='time',inplace=True)
    return ticks

def basic_sms(ticks):
    '''构造基本消息（当前价，开盘价，今日累计成交，10万以上成交占比）'''
    code_ = ticks.code.unique()[0]
    assert type(code_) == str, ('code_为单只股票代码，且必须是str')
    cur = ts.get_realtime_quotes(code_)
    name_ = cur.loc[0,'name']
    cp = float(cur.loc[0,'price']) # 当前价
    op = float(cur.loc[0,'open'])  # 开盘价
    today_amount  = cur.loc[0,'amount'].split('.')[0]  #今日累计成交
    # 10万以上成交占比
    ticks_10w = ticks[ticks.amount > 100000]
    amount_10w = sum(ticks_10w.amount)
    ratio_10w = amount_10w/float(today_amount)
    # 构造基本消息
    b_sms = '''{0}({1})当前价 {2}元，开盘价 {3}元，
    今日累计成交 {4}元，其中10万以上成交占比 {5}%\n''' \
    .format(code_,name_,cp,op,today_amount,str(ratio_10w*100)[0:5])
    return b_sms

def fixed_interval_inform(ticks,interval=10):
    '''固定时间间隔发送消息
    
    parameters
    -------------------
    ticks       get_tics的返回对象
    interval    固定时间间隔（单位：分钟）    
    '''
    if datetime.now().minute%interval == 0:
        # 调用basic_sms生成基本通知消息
        b_sms = basic_sms(ticks)
        sms = '【固定间隔通知】' + b_sms
        # 调用notifier发送消息
        notifier(bot,contacts,sms)
    
    
        
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
    sms1 = '【{0} · 波动预警 · {1}】\n全天波动：{2}%\n10分钟波动：{3}%\n5分钟波动{4}%' \
            .format(
                    code_,
                    str(datetime.now()).split('.')[0],
                    str(c_today*100)[0:5],
                    str(c_10min*100)[0:5],
                    str(c_5min*100)[0:5],
                    )
    sms2 = '\n今日累计成交量：%s \n'%today_amount
    sms = sms1 + sms2  
                  
    # 判断是否需要进行预警
    if c_today > mode['change_in_today']:
        send_sms = True
    elif c_5min > mode['change_in_5min']:
        send_sms = True
    elif c_10min > mode['change_in_10min']:
        send_sms = True
    else:
        send_sms = False

    sms_sended = False
    if send_sms:
        # 调用notifier发送预警消息
        notifier(bot,contacts,sms)
        sms_sended = True
    return sms_sended  # 发送消息之后，返回sms_sended为true

        
def m_big(ticks,mode_level='level_A'):
    '''监控大单
    
    parameter
    -----------------------------------------
    ticks  今日的历史分笔数据  pd.DataFrame
    mode_level 监控模式，详见conf.py

    example
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
    sms1 = '【{0} · 大单预警 · {1}】\n今日大单累计成交 {2} 元，占比 {3}%。\n最近几分钟，大单密集，请注意！' \
            .format(
                    code_,
                    str(datetime.now()).split('.')[0],
                    cumsum_big,
                    str(big_rate*100)[0:5],
                    )
    sms2 = '\n今日累计成交量：%s \n'%str(today_amount)
    sms = sms1 + sms2
    
    # 判断是否需要进行预警
    if bm_10min > mode['big_in_10min']:
        send_sms = True
    elif bm_5min > mode['big_in_5min']:
        send_sms = True
    else:
        send_sms = False
    
    sms_sended = False
    if send_sms:
        # 调用notifier发送预警消息
        notifier(bot,contacts,sms)
        sms_sended = True
    return sms_sended  # 发送消息之后，返回sms_sended为true
    
