# -*- coding: utf-8 -*-
"""实用工具集"""


"""
————————————————————————————————————————————————————————————————————————————————————

————————————————————————————————————————————————————————————————————————————————————
"""



"""
————————————————————————————————————————————————————————————————————————————————————
股票池对象
————————————————————————————————————————————————————————————————————————————————————
"""

class StockPool:
    """股票池对象

    example
    ------------

    """
    def __init__(self):
        self.pool = set()

    def add(self, stocks):
        """添加股票

        params
        ---------
        stocks      list or tuple
        """
        for stock in stocks:
            self.pool.add(stock)
        # return self.pool

    def remove(self, stocks):
        """删除股票

        params
        ---------
        stocks      list or tuple
        """
        for stock in stocks:
            self.pool.remove(stock)

    def empty(self):
        """清空股票池"""
        self.pool.clear()

    def is_empty(self):
        """判断股票池是否为空"""
        if len(self.pool) == 0:
            return True
        else:
            return False

    def to_list(self):
        """转换成list"""
        return list(self.pool)


def create_sp(stocks):
    """创建股票池对象

    params
    ----------
    stocks      list or tuple
    """
    sp = StockPool()
    sp.add(stocks)
    return sp


