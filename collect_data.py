# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import date
from apscheduler.schedulers.blocking import BlockingScheduler
# from Debug_A.stock_pool import create_sp
from Debug_A.data_collector import get_real_time
from Debug_A.data_collector import get_hist_ticks
import sqlite3
"""
————————————————————————————————————————————————————————————————————————————————————————
系统初始化
_________________________________________________________________________________________
"""
codes = ['sh', 'sz', '600122', '600977', '601611', '002256', '002631', '601595']
sched = BlockingScheduler()
conn = sqlite3.connect('market_A.db')
conn.close()

def collect_real_time(codes):
    F_real_time = './csv/real_time_%s.csv' % datetime.now().date().__str__()
    rt_data = get_real_time(codes, F_real_time)
    return rt_data


if __name__ == "__main__":
    start = date(2017, 8, 10)
    end = date(2017, 8, 20)
    hist = get_hist_ticks(codes=codes, start=start, end=end)
    # rt_data = collect_real_time(codes)
    hist.to_sql('hist_ticks', con=conn, if_exists='append', index=False)

