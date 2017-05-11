# -*- coding: utf-8 -*-
"""
Created on Thu May 11 13:53:10 2017

@author: Mike
"""
import threading
from single_monitor import single_monitor

# 使用多个线程，每个线程监控一只股票
m1 = threading.Thread(target=single_monitor,args=('600122',),name='htgk')
m2 = threading.Thread(target=single_monitor,args=('002256',),name='zxgf')

m1.start()
m2.start()
m1.join()
m2.join()
