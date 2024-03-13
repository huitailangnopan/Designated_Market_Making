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
        self.mm_orderbook = []
        self.matched_orders = []
        self.all_orders_updated = []

    def initialize_record(self):
        for table in ["market_trade", "price_his", "trade_book"]:
            with SqliteDict("exchange.sqlite", tablename=table, autocommit=True) as db:
                pass

    def run_next_round(self):
        self.price_bot.updatedOrderbookfromExchange(self.all_orders_updated)
        self.latest_orderbook = self.price_bot.get_newest_orderbook(real_mkt=self.real_mkt)
        self.current_time = self.price_bot.timestamp

    def update_markettradebook(self):
        orders_collection = []
        for i in self.latest_orderbook:
            orders_collection.append(i.__dict__())
        self.update_db("market_trade", orders_collection)


    def update_price(self):
        order_book = self.latest_orderbook
        price = self.calculate_price(order_book)
        self.update_db("price_his", price)
        self.price_history.append(price)

    def calculate_price(self, order_book):
        ask_prices = []
        bid_prices = []
        for i in order_book:
            if i.getordertype() == "SELL":
                ask_prices.append(i.getprice())
            if i.getordertype() == "BUY":
                bid_prices.append(i.getprice())
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

    def get_markettradebook(self):
        return self.latest_orderbook

    def get_mmtradebook(self):
        return self.mm_orderbook

    def mmtrade_submit(self):
        orders_collection = []
        for i in self.mm_orderbook:
            orders_collection.append(i.__dict__())
        self.update_db("trade_book", orders_collection)

    def update_db(self, table, data):
        with SqliteDict("exchange.sqlite", tablename=table, autocommit=True) as db:
            db[self.current_time] = data

    def exchange_execution(self):
        self.exchange.load_market(self.latest_orderbook)
        self.exchange.load_trade(self.mm_orderbook)
        self.exchange.update_time(self.current_time)
        self.matched_orders, self.all_orders_updated = self.exchange.exchange_execute()

    def send_book(self):
        mm_no = 1
        self.mm_orderbook = []
        for i in range(mm_no):
            self.mm_orderbook = trading_strategy(self.current_time, self.latest_orderbook, i)


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
