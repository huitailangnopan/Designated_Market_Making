import pandas as pd
import numpy as np
import os
from price_simulate import price_simulate
import optimal_MM
import yaml

class Agent:
    """
    Price API, receive trade, update portfolio
    """

    def __init__(self, tickers, num_mm):
        self.tickers = tickers
        self.transaction_path = r"Portfolio and Trade book\trade_book.yml"
        self.orderbook_path = r"Portfolio and Trade book\market_trade.yml"
        self.price_path =r"Portfolio and Trade book\price_his.yml"
        self.latest_orderbook = price_simulate.get_newest_orderbook()
        self.price_his = []
        self.num_mm = num_mm
        self.price_bot = price_simulate()

    def run_next_round(self):
        pass

    def update_tradebook(self):
        order_book = self.latest_orderbook
        

    def update_price(self):
        order_book = self.latest_orderbook
        price = (order_book['bid']+order_book['ask'])/2
        with open(self.price_path, 'r') as yamlfile:
            cur_yaml = yaml.safe_load(yamlfile)
            cur_yaml[self.tickers].append(price)
            self.price_his = cur_yaml
        with open(self.price_path, 'w') as yaml_file:
            yaml.dump(self.price_his, yaml_file, default_flow_style=False)

    def get_price(self, wanted_ticker, num_timestamps) -> dict:
        """
        return the price of the wanted tickers
        :param wanted_ticker: str: the symbol of the equity to acquire
        :param num_timestamps: number of timestamps of price
        :return: dict: a dictionary of dataframes
        """
        pass
    
    
