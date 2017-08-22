# -*- coding: utf-8 -*-

import os
import tushare as ts
from datetime import timedelta, datetime
import pandas as pd
from time import sleep
from urllib.error import URLError
# import self-defined module
from zb_CodeSet.Tools.logger import create_logger
from zb_CodeSet.Tools.sms import push_sms


F_log = './log/A_data_collector_%s.log' % datetime.now().date().__str__()
logger = create_logger(F_log, name='collector', cmd=True)


def get_hist_ticks(codes, start, end):
    """获取codes中所有股票从start到end的历史分笔数据

    example
    ------------------------------------------------
    start = date(2017, 8, 10)
    end = date(2017, 8, 20)
    get_hist_ticks(codes=codes, start=start, end=end)
    """
    csv = 'temp_hist_ticks.csv'
    # with open(csv, 'w', encoding='gbk') as f:
    #     f.write('')
    delta = timedelta(days=1)
    for code in codes:
        d_ = start
        while d_ <= end:
            # 调用ts获取历史分笔数据
            try:
                ticks = ts.get_tick_data(code, date=str(d_), retry_count=10)
                ticks['date'] = d_
                # ticks['code'] = '|' + code
                ticks['code'] = code
                ticks.to_csv(csv, index=False, mode='a', encoding='gbk')
                logger.info('{0} 在 {1} 的分笔数据获取成功！'.format(code, d_))
            except:
                logger.info('{0} 在 {1} 的分笔数据获取失败！'.format(code, d_))
            d_ = d_ + delta

    # 读取csv文件，去掉重复数据
    datas = pd.read_csv(csv, encoding='gbk')
    os.remove(csv)
    datas = datas.drop_duplicates().dropna()
    datas = datas[datas['time'] != 'time']
    datas = datas[['code', 'date', 'time', 'price', 'change', 'volume', 'amount', 'type']]
    datas = datas.sort_values(by=['code', 'date', 'time'])
    # datas.to_csv(csv, index=False, encoding='gbk')
    return datas


def get_real_time(codes, interval=3):
    """获取实时交易数据"""
    rt_data = pd.DataFrame()
    loop = True
    i = 1
    while loop:
        try:
            quotes = ts.get_realtime_quotes(codes)
            logger.info('第%i次获取成功' % i)
        except URLError as e:
            logger.error('实时交易数据获取失败，原因：%s', e)
        rt_data = rt_data.append(quotes, ignore_index=True)
        if datetime.now().hour == 11 & datetime.now().minute > 31:
            loop = False
        elif datetime.now().hour not in [9, 10, 11, 13, 14]:
            loop = False
        else:
            sleep(interval)
    logger.info('当前阶段交易数据获取完成')
    rt_data.drop_duplicates(subset=['price', 'amount'], inplace=True)
    return rt_data


if __name__ == '__main__':
    pass



