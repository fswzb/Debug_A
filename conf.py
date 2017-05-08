# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 12:34:34 2017

@author: Mike
"""

# 监控模式  level_A  强  level_B 一般  level_C 弱
modes = {'level_A':{
                    # 涨跌幅监控参数
                    'change_in_today':0.05,       # 5%
                    'change_in_10min':0.03,       # 3%
                    'change_in_5min':0.01,       # 1%
                    # 大单监控参数
                    'over':[100000,200000,500000,1000000,5000000],
                    'big_in_5min':10,
                    'turnover_rate_in_5min':0.05  # 5%
                    },
         'level_B':{
                    'over':[200000,500000,1000000,5000000],
                    'change_in_10min':0.01,       # 1%
                    'big_num_in_5min':10,
                    'turnover_rate_in_5min':0.05  # 5%
                    },
         'level_C':{
                    'over':[500000,1000000,5000000],
                    'change_in_10min':0.01,       # 1%
                    'big_num_in_5min':10,
                    'turnover_rate_in_5min':0.05  # 5%
                    }
        }

# 需要监控的股票列表 必须为list
codes = ['600122']

# 接收监控消息的联系人
contacts = ['年轻人','great']

time_span = ['13:00','15:00']

def QQ_login():
    '''
    登录QQ机器人用于发送消息
    
    调用该函数之后会弹出一个二维码，使用用于发送消息的QQ扫码登录即可
    name 为 用于接收监控消息的qq备注名，即已登录QQ中的任一个好友
    '''
    from qqbot import QQBot
    bot = QQBot()
    bot.Login()  # 用需要登录的qq扫码
    return bot