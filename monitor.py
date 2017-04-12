# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 21:21:27 2017

@author: Mike
"""

import tushare as ts
from datetime import datetime,date,time,timedelta
import time as t

from functions import xq_code_url,open_url


class monitor:
    '''
    盘中监控器
    
    监控器初始化参数：
        股票代码  code  
        大单定义  over  默认值 100000
        开始时间  time_s
        结束时间  time_e
        
    '''
    def __init__(self,code,over=100000):
        self.version = 'test'
        self.author = 'zb'
        self.date = datetime.today().date()
        self.code = code
        self.url = xq_code_url(code)
        # over是对大单的定义，即成交总额超过over的会被认为是大单
        self.over = over
        self.open_p = float(ts.get_realtime_quotes(code).iloc[0,1])
        
    def check_undulation_and_num_big(self,time_span=5,change=0.01,num_big=10):
        '''
        检测5分钟波动1%以上；检测5分钟大单数量。
        
        '''
        code = self.code
        over = self.over        
        url = self.url
        
        delta = timedelta(minutes=time_span)
        open_p = self.open_p       
        
        print('正在监控：%s'%code)
        while time(9,30,0) <= datetime.now().time() <= time(11,30,0) or \
              time(13,0,0) <= datetime.now().time() <= time(15,0,0) :
            
            # 调用ts.get_today_ticks获取当日历史分笔
            ticks = ts.get_today_ticks(code)
            ticks['time'] = [datetime.strptime(ticks.iloc[i,0],'%H:%M:%S') \
                                for i in range(len(ticks))]
            # 选择从当前时间开始五分钟内的数据
            dt = datetime.combine(date(1900,1,1),datetime.now().time())
            s_dt = dt - delta
            datas = ticks[ticks.time > s_dt]
            
            # 计算5分钟波动 
            datas['price'] = [float(i) for i in datas['price']]
            p_wave = (max(datas.price) - min(datas.price))/open_p
            p_wave = round(p_wave,3)
            if p_wave > change:
                open_url(url)
                t.sleep(120)
            
            # 检测5分钟大单数量
            big_orders = datas[datas.amount > over]
            if len(big_orders) > num_big:
                open_url(url)
                t.sleep(120)
            
            t.sleep(30)
        print('监控结束：%s'%code)
    
    def check_big_order(self,over=100000,to_csv=True):
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
        code = self.code
        
        # 调用ts.get_today_ticks获取当日交易记录
        ticks = ts.get_today_ticks(code)
        
        # 获取当日成交额
        amount = float(ts.get_realtime_quotes(code).iloc[0,9])
        datas = ticks[ticks.amount > over]
        bs = dict(datas.groupby(['type']).apply(sum)['amount'])
        print(bs)
        ratio = sum(bs.values())/amount
        print('{0}万以上成交量占比：{1}'.format(str(over)[0:2],round(ratio,3)))
        
        # 保存结果
        if to_csv == True:
            res_csv = code + '_over_' + str(over)[0:2] + 'w_'+\
                        date.today().isoformat()+'.csv'
            datas.to_csv(res_csv, index=False)
        
        return datas
        
        
        
    
