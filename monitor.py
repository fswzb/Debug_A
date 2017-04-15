# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 21:21:27 2017

@author: Mike
"""

import tushare as ts
from datetime import datetime,date,time,timedelta
import time as t



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
        # over是对大单的定义，即成交总额超过over的会被认为是大单
        self.over = over
        self.open_p = float(ts.get_realtime_quotes(code).iloc[0,1])
        
        # 登录QQ机器人
        from qqbot import QQBot
        self.bot = QQBot()
        self.bot.Login()  # 用需要登录的qq扫码
        self.con = self.bot.List('buddy','年轻人')  # 获取好友列表
        sms = 'QQ机器人登录成功！'
        self.bot.SendTo(self.con[0],sms)        
    
    def sms_contruct(code,ticks,over=100000):
        '''
        构造通知消息
        
        parameters
        ----------
            code    股票代码
            ticks   股票当日历史分笔，dataframe
        '''
        # 时间
        dt = datetime.now().isoformat(' ').split('.')[0]
        # 当前价 & 当前量
        rt = ts.get_realtime_quotes(code)
        price = rt.iloc[0,3]
        amount = float(rt.iloc[0,9])
        # 10万以上买卖盘分布及其占比
        datas = ticks[ticks.amount > over]
        bs = dict(datas.groupby(['type']).apply(sum)['amount'])
        ratio = sum(bs.values())/amount
        # 构造sms
        sms_1 = '{0}\n{1}：当前价 {2},当前总成交 {3}\n'.format(dt,code,price,amount)
        sms_2 = '{0}万以上成交量占比 {1}；其中，买盘 {2}，卖盘{3}'.format(str(over)[0:2],
                round(ratio,3),bs['买盘'],bs['卖盘'])
        return sms_1 + sms_2
        
    
    def check_undulation_and_num_big(self,time_span=5,change=0.01,num_big=10):
        '''
        检测5分钟波动1%以上；检测5分钟大单数量。
        
        '''
        code = self.code
        over = self.over
        
        delta = timedelta(minutes=time_span)
        open_p = self.open_p       
        
        print('正在监控：%s'%code)
        while time(9,30,0) <= datetime.now().time() <= time(11,30,0) or \
              time(13,0,0) <= datetime.now().time() <= time(15,0,0) :
            
            # 调用ts.get_today_ticks获取当日历史分笔
            ticks = ts.get_today_ticks(code,retry_count=10)
            print('\n')
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
                sms = monitor.sms_contruct(code,ticks,over)
                self.bot.SendTo(self.con[0],sms)
                t.sleep(120)
            
            # 检测5分钟大单数量
            big_orders = datas[datas.amount > over]
            if len(big_orders) > num_big:
                sms = monitor.sms_contruct(code,ticks,over)
                self.bot.SendTo(self.con[0],sms)
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
        print('\n')
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
        
        
        
    
