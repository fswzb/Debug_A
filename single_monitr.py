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
code = conf.code
contacts = conf.contacts
mode = conf.modes['level_A']
bot = conf.QQ_login()

class single_monitor:
    '''单只股票监控'''
    def __init__(self,bot,code,contacts,mode):
        self.bot = bot
        self.code = code
        self.contacts = contacts
        self.mode = mode
    
    def save_realtime_quotes(self,csv = 'realtime_quotes.csv'):
        '''获取实时分笔数据，并保存到csv中'''
        code = self.code
        try:
            rq = ts.get_realtime_quotes(code)
            rq.to_csv(csv,index=False,mode='a',header=False)
            return rq
        except:
            dt = datetime.now().isoformat().split('.')[0]
            print('{0}:\n{1} 实时分笔数据获取失败'.format(dt,code))
            
    def main(self):
        code = self.code
        print('正在监控：%s'%code)
        while time(9,30,0) <= datetime.now().time() <= time(11,30,0) or \
              time(13,0,0) <= datetime.now().time() <= time(15,0,0) :
            single_monitor.save_realtime_quotes(self,csv = 'realtime_quotes.csv')
            t.sleep(5)
    
m = single_monitor(bot,code,contacts,mode)