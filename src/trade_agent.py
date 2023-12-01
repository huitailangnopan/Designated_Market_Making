import pandas as pd
import numpy as np
import os
from src.price_simulate import price_simulate
import yaml
from sqlitedict import SqliteDict
from src.optimalMM import trading_strategy

class Agent:
    """
    Price API, receive trade, update portfolio
    """

    def __init__(self, tickers,num_mm,real_mkt):
        self.tickers = tickers # single tickers
        self.path = r"Portfolio and Trade book\exchange.sqlite"
        self.price_bot = price_simulate()
        self.real_mkt = real_mkt
        self.latest_orderbook = self.price_bot.get_newest_orderbook(real_mkt = self.real_mkt)
        self.current_time = self.price_bot.timestamp
        self.price_history = []
        self.num_mm = num_mm  #set numbers of MM
        self.initialize_record()
        
    def initialize_record(self):
        market_trade = SqliteDict("exchange.sqlite", tablename="market_trade", autocommit=True)       
        price_his = SqliteDict("exchange.sqlite", tablename="price_his", autocommit=True)
        trade_book = SqliteDict("exchange.sqlite", tablename="trade_book", autocommit=True)
        market_trade.close()
        price_his.close()
        trade_book.close()
                  
    def run_next_round(self):
        self.latest_orderbook = self.price_bot.get_newest_orderbook(real_mkt = self.real_mkt)
        self.current_time = self.price_bot.timestamp

    def update_tradebook(self) -> None:
        order_book = self.latest_orderbook
        db = SqliteDict("exchange.sqlite",tablename="market_trade")
        db_copy = {self.tickers:order_book}
        db[self.current_time] = db_copy
        db.commit()
        db.close()
                     
    def update_price(self) -> None:
        order_book = self.latest_orderbook
        price = (order_book['bid1_price']+order_book['ask1_price'])/2
        db = SqliteDict("exchange.sqlite",tablename="price_his")
        db[self.current_time] = price
        db.commit()
        db.close()
    
    def get_orderbook(self) -> dict:
        return self.latest_orderbook

    def get_price(self, wanted_ticker, num_timestamps) -> dict:
        """
        return the price of the wanted tickers
        :param wanted_ticker: str: the symbol of the equity to acquire
        :param num_timestamps: number of timestamps of price
        :return: dict: a dictionary of dataframes
        """
        with open(self.price_path, 'r') as yamlfile:
            cur_yaml = yaml.safe_load(yamlfile)
            price = cur_yaml[wanted_ticker].values()[-num_timestamps:]
            return price
         
    def trade_submit(self) -> None:
        db = SqliteDict("exchange.sqlite",tablename="mm1")
        db_copy = db[self.current_time]
        db.close()
        db = SqliteDict("exchange.sqlite",tablename="trade_book")
        db[self.current_time] = db_copy
        db.commit()
        db.close()
        
    def send_book(self):
        trading_strategy(self.current_time)