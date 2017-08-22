# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 12:58:27 2017

@author: Mike
"""
import matplotlib.pyplot as plt
import tushare as ts

# 获取行情数据
data = ts.get_k_data(code='600122', start='2016-12-12', end='2017-04-17')
data['date'] = []


def show_data(data):
    close_data = data['close']
    plt.autoscale(True, 'both', None)
    # 绘制方格
    plt.rc('axes', grid=True)
    plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
    plt.plot(data['date'], close_data)
    # 设置坐标标签
    plt.xlabel('Date')
    plt.ylabel('Close')
    # 将x坐标日期进行倾斜
    plt.setp(plt.gca().get_xticklabels(), rotation=20, horizontalalignment='right')
    plt.show()
