# Debug_A
A股盯盘机器人，主要功能：检测交易时间股票价格、成交量的的异常情况。

## Test
    from monitor import monitor
    m = monitor('600122')
    m.check_undulation_and_num_big()
