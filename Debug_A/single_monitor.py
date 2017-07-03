# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 11:00:36 2017

@author: Mike
"""

from datetime import datetime,time
from time import sleep
import monitor as m

def single_monitor(code,high,low,interval):
    '''监控单只股票的大单和波动'''
    print('时间：%s   正在监控 %s'%(str(datetime.now()).split('.')[0],code))
    while time(9,30,0) <= datetime.now().time() <= time(11,30,0) or \
        time(13,0,0) <= datetime.now().time() <= time(15,0,0) :
        # 股价监控
        m.m_price(code,high=high,low=low)
        ticks = m.get_ticks(code)
        # 固定间隔通知
        m.fixed_interval_inform(ticks,interval=interval)
        # 监控波动和大单
        sms_sended1 = m.m_change(ticks,mode_level='level_A')
        sms_sended2 = m.m_big(ticks,mode_level='level_A')
        sleep(3)
        # 一条预警消息发送之后，程序休眠 120秒
        if sms_sended1 or sms_sended2:
            sleep(120)
        
if __name__ == '__main__':
	code = '600122'
	single_monitor(code)
