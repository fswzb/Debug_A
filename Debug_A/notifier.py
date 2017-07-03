# -*- coding: utf-8 -*-
"""
Created on Mon May 15 14:29:08 2017

@author: Mike
"""

'''
-------------------------------------------------------------------------------
QQ消息发送模块
-------------------------------------------------------------------------------
'''
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
    
bot = QQ_login(qq='1257391203')
contacts = ['年轻人']  # 使用QQ发送消息，同时向多个联系人发送消息会被封号。


'''
-------------------------------------------------------------------------------
邮件消息发送模块
-------------------------------------------------------------------------------
'''
def email_login(user = 'zeng_bin8888@163.com',pwd = 'why1257391203'):
    '''登录邮箱（测试使用的是163邮箱）
    邮箱必须开启smtp服务
    
    '''
    import smtplib  
    smtp=smtplib.SMTP()  
    smtp.connect('smtp.163.com','25')  
    smtp.login(user=user,password=pwd)
    return smtp
    
def send_eamil(smtp,from_,to_,subject_,content):
    '''发送email预警消息
    
    parameters
    ------------
    smtp        email_login的返回对象，即已经登录的邮箱
    from_       发件邮箱
    to_         收件邮箱
    subject_    邮件主题
    content     邮件内容
    
    '''
    import email 
    
    # 构造消息
    msg = email.mime.multipart.MIMEMultipart()  
    msg['from'] = from_ 
    msg['to'] = to_
    msg['subject'] = subject_  
    txt=email.mime.text.MIMEText(content)  
    msg.attach(txt)
    
    # 发送
    smtp.sendmail(from_,to_,str(msg))  
    #smtp.quit()

