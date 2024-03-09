import pandas as pd
import numpy as np
import os
from src.price_simulate import price_simulate
import yaml
from sqlitedict import SqliteDict
from src.optimalMM import trading_strategy
import os
from src.exchange import exchange


class Agent:
    """
    The Agent class simulates a trading agent in a designated market making scenario.
    It handles interactions with market data, manages the trading book, and executes trades
    based on orders from various market makers
    """

    def __init__(self, tickers, num_mm, real_mkt):
        self.tickers = tickers  # single tickers
        self.path = r"Portfolio and Trade book\exchange.sqlite"
        self.price_bot = price_simulate()
        self.real_mkt = real_mkt
        self.latest_orderbook = self.price_bot.get_newest_orderbook(real_mkt=self.real_mkt)
        self.last_time = None
        self.current_time = self.price_bot.timestamp
        self.price_history = []
        self.num_mm = num_mm  # set numbers of MM
        self.initialize_record()
        self.exchange = exchange()

    def initialize_record(self):
        """Initializes the trading record in the database."""
        market_trade = SqliteDict("exchange.sqlite", tablename="market_trade", autocommit=True)
        price_his = SqliteDict("exchange.sqlite", tablename="price_his", autocommit=True)
        trade_book = SqliteDict("exchange.sqlite", tablename="trade_book", autocommit=True)
        market_trade.close()
        price_his.close()
        trade_book.close()

    def run_next_round(self):
        """Run the next timestamp of the market"""
        self.latest_orderbook = self.price_bot.get_newest_orderbook(real_mkt=self.real_mkt)
        self.last_time = self.current_time
        self.current_time = self.price_bot.timestamp

    def update_tradebook(self) -> None:
        """
        Updates the trade book with a new trade.
        """
        order_book = self.latest_orderbook
        db = SqliteDict("exchange.sqlite", tablename="market_trade")
        db_copy = {self.tickers: order_book}
        db[self.current_time] = db_copy
        db.commit()
        db.close()

    def update_price(self) -> None:
        """Updates the price based on the latest market data."""
        # price = (bid+ask)/2
        order_book = self.latest_orderbook
        if order_book['bid1_price'] * order_book['ask1_price'] != 0:
            price = (order_book['bid1_price'] + order_book['ask1_price']) / 2
            price = round(price, 2)
        else:
            price = self.proxy_price(self.price_history)
        db = SqliteDict("exchange.sqlite", tablename="price_his")
        db[self.current_time] = price
        db.commit()
        db.close()
        self.price_history.append(price)

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

    def get_orderbook(self) -> dict:
        """Get current order book"""
        return self.latest_orderbook

    def trade_submit(self) -> None:
        """
        conclude orders from all market makers
        """
        db = SqliteDict("exchange.sqlite", tablename="mm1")
        db_copy = db[self.current_time]
        db.close()
        db = SqliteDict("exchange.sqlite", tablename="trade_book")
        db[self.current_time] = db_copy
        db.commit()
        db.close()

    def exchange_execution(self):
        pass

    def send_book(self):
        """send the current market book to each MM"""
        trading_strategy(self.current_time)
