import pandas as pd
import numpy as np
from src.price_simulate import PriceSimulator
from sqlitedict import SqliteDict
from src.optimalMM import trading_strategy
from src.exchange import exchange


class Agent:
    def __init__(self, tickers, num_mm, real_mkt):
        self.tickers = tickers
        self.price_bot = PriceSimulator()
        self.real_mkt = real_mkt
        self.latest_orderbook = self.price_bot.get_newest_orderbook(real_mkt=self.real_mkt)
        self.current_time = self.price_bot.timestamp
        self.price_history = []
        self.num_mm = num_mm
        self.initialize_record()
        self.exchange = exchange()

    def initialize_record(self):
        for table in ["market_trade", "price_his", "trade_book"]:
            with SqliteDict("exchange.sqlite", tablename=table, autocommit=True) as db:
                pass

    def run_next_round(self):
        self.latest_orderbook = self.price_bot.get_newest_orderbook(real_mkt=self.real_mkt)
        self.current_time = self.price_bot.timestamp

    def update_tradebook(self):
        self.update_db("market_trade", {self.tickers: self.latest_orderbook})

    def update_price(self):
        order_book = self.latest_orderbook
        price = self.calculate_price(order_book)
        self.update_db("price_his", price)
        self.price_history.append(price)

    def calculate_price(self, order_book):
        if len(order_book['bid_price']) * len(order_book['ask_price']) != 0:
            return round((max(order_book['bid_price']) + min(order_book['ask_price'])) / 2, 2)
        else:
            return self.proxy_price(self.price_history)

    def proxy_price(self, price_history):
        # Iterate backwards to find the first non-zero price
        for price in reversed(price_history):
            if price != 0:
                return price
        return 0

    def get_orderbook(self):
        return self.latest_orderbook

    def trade_submit(self):
        with SqliteDict("exchange.sqlite", tablename="mm1") as db:
            self.update_db("trade_book", db[self.current_time])

    def update_db(self, table, data):
        with SqliteDict("exchange.sqlite", tablename=table, autocommit=True) as db:
            db[self.current_time] = data

    def exchange_execution(self):
        pass

    def send_book(self):
        trading_strategy(self.current_time)


'''
    def proxy_price(self, price_history):
        """To prevent price to be zero when there's no order"""
        if len(price_history) == 0:
            return 0
        if price_history[-1] == 0:
            if len(price_history) == 1:
                return 0
            else:
                return self.proxy_price(price_history[:len(price_history) - 1])
        else:
            return price_history[-1]
'''
