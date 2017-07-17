# Debug_A -- A股盯盘机器人

## 简介

A股变化莫测，光靠一双眼睛、四台显示器盯盘难免会有疏漏。如果能有个程序，
模拟人的盯盘动作，实时监控盘面变化，一旦发现“异常变化”还能发送预警消息，
那就再好不过了。本项目的目标就是实现这样一个程序，即实现A股交易时间自动
盯盘，检测到“异常情况”，实时发送QQ消息或者邮件进行通知。

最近准备对该项目进行重构，历史版本见 history/Debug_A_V1.0


## 项目实现功能

1. 记录所监控股票的盘口数据，用于收盘后分析
2. 大单成交实时监控
3. 股价波动实时监控
4. QQ消息实时发送
5. 邮件预警消息发送

## 项目依赖

- [pandas](http://pandas.pydata.org/)
- [tushare](https://github.com/waditu/tushare)
- [QQbot](https://github.com/pandolia/qqbot)
- [APScheduler](http://apscheduler.readthedocs.io/en/latest/)

