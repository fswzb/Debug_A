# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 11:00:36 2017

@author: Mike
"""

import tushare as ts
from datetime import datetime,date,time,timedelta
import time as t
import monitor as m

# 需要监控的股票列表 必须为list
codes = ['600122']
ticks = m.get_ticks(codes[0])

m.m_change(ticks,mode_level='level_C')
m.m_change(ticks,mode_level='level_C')






