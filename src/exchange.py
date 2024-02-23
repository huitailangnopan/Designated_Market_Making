import pandas as pd
import numpy as np
from sqlitedict import SqliteDict
from src.utils.analysis import sql_to_list,sql_to_pd

class exchange:
    def __int__(self,time):
        self.current_time = time
        self.marketorder = None
        self.tradeorder = None

    def load_market(self):
        """
        change_todo: change the dict key from sql_to_pd to a column in df, add the time index as well
        """
        self.marketorder = SqliteDict("exchange.sqlite", tablename="market_trade")

    def load_trade(self):
        self.tradeorder = SqliteDict("exchange.sqlite",tablename="trade_book")