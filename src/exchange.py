import pandas as pd
import numpy as np
from sqlitedict import SqliteDict
from src.utils.analysis import sql_to_list,sql_to_pd

class exchange:
    def __int__(self):
        self.marketorder = None
        self.tradeorder = None

    def update_time(self,time):
        self.current_time = time

    def load_assets(self, assets):
        self.assets = assets

    def load_market(self):
        """
        change_todo: change the dict key from sql_to_pd to a column in df, add the time index as well
        """
        self.marketorder = SqliteDict("exchange.sqlite", tablename="market_trade")
        self.marketorder = self.marketorder[self.current_time]
        self.marketorder = self.marketorder[self.assets]

    def load_trade(self):
        self.tradeorder = SqliteDict("exchange.sqlite",tablename="trade_book")
        self.tradeorder = self.tradeorder[self.current_time]
        self.tradeorder = self.tradeorder[self.assets]

    def exchange_execute(self):
        """
        match the orders in the market order book and trade order book
        """
        self.load_market()
        self.load_trade()


    