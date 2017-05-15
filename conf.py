# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 12:34:34 2017

@author: Mike
"""

'''
-------------------------------------------------------------------------------
监控条件配置模块
-------------------------------------------------------------------------------
'''
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
                    }
        }


# 登录QQ并指定接收监控消息的联系人
def QQ_login(qq = None,user = None):
    '''
    登录QQ机器人用于发送消息
    
    parameters
    -------------
    qq      需要登录的QQ号
    user    需要登录的QQ用户名
    注：qq和user传入一个参数就可以
    
    example
    -------------
    bot = QQ_login(qq='1145343044')
    
    '''
    from qqbot import QQBot
    bot = QQBot()
    bot.Login(qq=qq,user=user)  # 用需要登录的qq扫码
    return bot
    
bot = QQ_login(user='Debug_A')
contacts = ['年轻人']  # 使用QQ发送消息，同时向多个联系人发送消息会被封号。
