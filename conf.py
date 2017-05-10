# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 12:34:34 2017

@author: Mike
"""

# 监控模式  level_A  强  level_B 一般  level_C 弱
modes = {'level_A':{
                    # 波动监控参数
                    'change_in_today':0.05,       # 日波动5%
                    'change_in_10min':0.03,       # 10分钟波动3%
                    'change_in_5min':0.01,        # 5分钟波动1%
                    # 大单监控参数
                    'over':[100000,200000,500000,1000000,5000000],
                    'big_in_5min':8,
                    'big_in_10min':16,
                    # 其他监控参数
                    'inform_interval':10       # 固定通知的时间间隔（分钟）
                    },
         'level_B':{
                    # 波动监控参数
                    'change_in_today':0.05,       # 日波动5%
                    'change_in_10min':0.03,       # 10分钟波动3%
                    'change_in_5min':0.01,        # 5分钟波动1%
                    # 大单监控参数
                    'over':[100000,200000,500000,1000000,5000000],
                    'big_in_5min':8,
                    'big_in_10min':16,
                    # 其他监控参数
                    'inform_interval':10       # 固定通知的时间间隔（分钟）
                    },
         'level_C':{  # 最低等级，开发阶段用于测试(任何时候都会触发预警)
                    # 波动监控参数
                    'change_in_today':0.03,       # 日波动5%
                    'change_in_10min':0.02,       # 10分钟波动3%
                    'change_in_5min':0.01,        # 5分钟波动1%
                    # 大单监控参数
                    'over':[100000,200000,500000,1000000,5000000],
                    'big_in_5min':5,
                    'big_in_10min':10,
                    # 其他监控参数
                    'inform_interval':10       # 固定通知的时间间隔（分钟）
                    }
        }


# 登录QQ并指定接收监控消息的联系人
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
    
bot = QQ_login()
contacts = ['年轻人','great']


