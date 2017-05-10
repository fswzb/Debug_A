# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 11:00:36 2017

@author: Mike
"""

from datetime import datetime,time
from time import sleep
import monitor as m

# 需要监控的股票列表 必须为list
codes = ['600122']
while time(9,30,0) <= datetime.now().time() <= time(11,30,0) or \
    time(13,0,0) <= datetime.now().time() <= time(15,0,0) :
    ticks = m.get_ticks(codes[0])
    sms_sended1 = m.m_change(ticks,mode_level='level_A')
    sms_sended2 = m.m_big(ticks,mode_level='level_A')
    while sms_sended1 or sms_sended1:
        sleep(180)
    sleep(3)






