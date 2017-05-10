# Debug_A -- A股盯盘机器人
**********************************************************************
## 简介
**********************************************************************
A股变化莫测，光靠一双眼睛、四台显示器盯盘难免会有疏漏。如果能有个程序，
模拟人的盯盘动作，实时监控盘面变化，一旦发现“异常变化”还能发送预警消息，
那就再好不过了。本项目的目标就是实现这样一个程序，即实现A股交易时间自动
盯盘，检测到“异常情况”，实时发送QQ消息或者邮件进行通知。

## 项目实现功能
**********************************************************************
1. 记录所监控股票的盘口数据，用于收盘后分析
2. 大单成交实时监控
3. 股价波动实时监控
4. QQ消息实时发送

## 项目依赖
**********************************************************************
- pandas
- tushare
- QQbot
- APScheduler

## 单只股票监控
**********************************************************************
	from datetime import datetime,time
	from time import sleep
	import monitor as m
	from conf import modes

	def single_monitor(code):
	    '''监控单只股票的大单和波动'''
	    
	    print('时间：%s   正在监控 %s'%(str(datetime.now()).split('.')[0],code))
	    while time(9,30,0) <= datetime.now().time() <= time(11,30,0) or \
	        time(13,0,0) <= datetime.now().time() <= time(15,0,0) :
	        ticks = m.get_ticks(codes[0])
	        sms_sended1 = m.m_change(ticks,mode_level='level_A')
	        sms_sended2 = m.m_big(ticks,mode_level='level_A')
	        sleep(3)
	        # 一条预警消息发送之后，程序休眠 120秒
	        while sms_sended1 or sms_sended2:
	            sleep(120)
	            sms_sended1 = False
	            sms_sended2 = False
	        
	if __name__ == '__main__':
		code = '600122'
		single_monitor(code)




