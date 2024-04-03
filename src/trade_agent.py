import random

import pandas as pd
import numpy as np
from src.price_simulate import PriceSimulator
from sqlitedict import SqliteDict
from src.optimalMM import marketmarker
from src.exchange import exchange


class Agent:
    def __init__(self, tickers, num_mm, real_mkt, num_rounds):
        """
        Initialize the Agent class with the given parameters.

        Parameters:
        tickers (list): List of tickers the agent is trading.
        num_mm (int): Number of market makers.
        real_mkt (bool): If True, use real market data. If False, simulate market data.
        num_rounds (int): Number of rounds the agent will trade.
        """
        self.num_rounds = num_rounds
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
        self.unsettled_orders = []
        self.playersIC = {}
        self.matched_orders_record = {"Time":[],"Matched Price":[],"Matched Quantity":[],"Buyer":[],"Seller":[]}
        self.all_orders_record = {"order_id":[],"customer_id":[],"order_time":[],
                                  "asset":[],"order_type":[],"order_price":[],"order_quantity":[],"total_amount":[],"status":[]}
        self.liquidity = {"qs":[],"DB":[]}
        self.mm_list = []
        self.initialize_mm()
        self.mm1 = marketmarker(1)

    def initialize_mm(self):
        """
        Initialize list of market maker.
        """
        for i in range(1,self.num_mm+1):
            self.mm_list.append(marketmarker(i))
    def initialize_record(self):
        """
        Initialize the database tables for the agent.
        """
        for table in ["market_trade", "price_his", "trade_book"]:
            with SqliteDict("exchange.sqlite", tablename=table, autocommit=True) as db:
                pass

    def run_next_round(self):
        """
        Run the next round of trading.
        """
        self.latest_orderbook = []
        self.price_bot.updatedOrderbookfromExchange(self.matched_orders,self.unsettled_orders)
        self.latest_orderbook.extend(self.price_bot.get_newest_orderbook(real_mkt=self.real_mkt))
        self.current_time = self.price_bot.timestamp

    def update_markettradebook(self):
        """
        Update the market trade book with the latest order book.
        """
        orders_collection = []
        for i in self.latest_orderbook:
            orders_collection.append(i.__dict__())
        self.update_db("market_trade", orders_collection)

    def update_price(self):
        """
        Update the price based on the latest order book.
        """
        order_book = self.unsettled_orders
        price = self.calculate_price(order_book)
        self.update_db("price_his", price)
        self.price_history.append(price)
        return price

    def calculate_price(self, order_book):
        """
        Calculate the price based on the order book.

        Parameters:
        order_book (list): The current order book.

        Returns:
        float: The calculated price.
        """
        ask_prices = []
        bid_prices = []
        for i in order_book:
            if i.getordertype() == "SELL":
                ask_prices.append(i.order_price)
            if i.getordertype() == "BUY":
                bid_prices.append(i.order_price)
        if len(bid_prices) * len(ask_prices) != 0:
            return round((max(bid_prices) + min(ask_prices)) / 2, 2)
        else:
            return self.proxy_price(self.price_history)

    def proxy_price(self, price_history):
        """
        Get the proxy price from the price history.

        Parameters:
        price_history (list): The history of prices.

        Returns:
        float: The proxy price.
        """
        # Iterate backwards to find the first non-zero price
        for price in reversed(price_history):
            if price != 0:
                return price
        return 0

    def get_markettradebook(self):
        """
        Get the latest market trade book.

        Returns:
        list: The latest market trade book.
        """
        return self.latest_orderbook

    def get_mmtradebook(self):
        """
        Get the market maker trade book.

        Returns:
        list: The market maker trade book.
        """
        return self.mm_orderbook

    def mmtrade_submit(self):
        """
        Submit the market maker trade.
        """
        orders_collection = []
        for i in self.mm_orderbook:
            orders_collection.append(i.__dict__())
        self.update_db("trade_book", orders_collection)

    def update_db(self, table, data):
        """
        Update the database with the given data.

        Parameters:
        table (str): The table to update.
        data (dict): The data to update the table with.
        """
        with SqliteDict("exchange.sqlite", tablename=table, autocommit=True) as db:
            db[self.current_time] = data

    def extract_unsettled_orders(self):
        """
        Extract the unsettled orders from the market trade book after the exchange.
        """
        self.unsettled_orders = []
        for i in self.all_orders_updated:
            if i.status == "PENDING":
                self.unsettled_orders.append(i)

    def exchange_execution(self):
        """
        Execute the exchange.
        """
        self.exchange.load_trade(self.mm_orderbook)
        self.exchange.load_market(self.latest_orderbook)
        self.exchange.update_time(self.current_time)
        self.matched_orders, self.all_orders_updated = self.exchange.exchange_execute()
        self.extract_unsettled_orders()
        self.liquidity_analysis()
        self.record_playerIC()
        self.record_matched_orders()
        self.record_all_orders()

    def liquidity_analysis(self):
        """
        Analyze the liquidity.
        """
        mt = self.update_price()
        # Filter the unsettled orders to only include 'SELL' orders
        sell_orders = [order for order in self.unsettled_orders if order.getordertype() == 'SELL']

        # Use the min function with a key argument to find the order with the minimum price
        min_sell_order = min(sell_orders, key=lambda order: order.getorderprice(), default=None)

        # Get the quantity of that order
        if min_sell_order is not None:
            min_sell_order_quantity = min_sell_order.getorderquantity()
            min_sell_order_price = min_sell_order.getorderprice()
        else:
            min_sell_order_quantity = 0
            min_sell_order_price = 0

        # Filter the unsettled orders to only include 'BUY' orders
        buy_orders = [order for order in self.unsettled_orders if order.getordertype() == 'BUY']

        # Use the max function with a key argument to find the order with the maximum price
        max_buy_order = max(buy_orders, key=lambda order: order.getorderprice(), default=None)

        # Get the quantity of that order
        if max_buy_order is not None:
            max_buy_order_quantity = max_buy_order.getorderquantity()
            max_buy_order_price = max_buy_order.getorderprice()
        else:
            max_buy_order_quantity = 0
            max_buy_order_price = 0

        if max_buy_order_price*min_sell_order_price != 0:
            qs = (min_sell_order_price - max_buy_order_price) / mt
        else:
            qs = 0
        DB = min_sell_order_quantity + max_buy_order_quantity
        self.liquidity["qs"].append(qs)
        self.liquidity["DB"].append(DB)



    def record_playerIC(self):
        for i in range(1, self.num_mm + 1):
            self.playersIC["mm" + str(i) + "_inventory"] = self.mm_list[i - 1].inventory_history
            self.playersIC["mm" + str(i) + "_cash"] = self.mm_list[i - 1].cash_history
        self.playersIC["p1_inventory"], self.playersIC["p1_cash"], self.playersIC["p3_inventory"], self.playersIC[
            "p3_cash"] = self.price_bot.record_participants()
        self.playersIC["price_history"] = self.price_history
    def record_matched_orders(self):
        """
        Record the matched orders.
        """
        for i in self.matched_orders:
            self.matched_orders_record["Time"].append(i["Time"])
            self.matched_orders_record["Matched Price"].append(i["Matched Price"])
            self.matched_orders_record["Matched Quantity"].append(i["Matched Quantity"])
            self.matched_orders_record["Buyer"].append(i["Buyer"])
            self.matched_orders_record["Seller"].append(i["Seller"])

    def record_all_orders(self):
        """
        Record all the orders.
        """
        for i in self.all_orders_updated:
            i = i.__dict__()
            self.all_orders_record["order_id"].append(i["order_id"])
            self.all_orders_record["customer_id"].append(i["customer_id"])
            self.all_orders_record["order_time"].append(i["order_time"])
            self.all_orders_record["asset"].append(i["asset"])
            self.all_orders_record["order_type"].append(i["order_type"])
            self.all_orders_record["order_price"].append(i["order_price"])
            self.all_orders_record["order_quantity"].append(i["order_quantity"])
            self.all_orders_record["total_amount"].append(i["total_amount"])
            self.all_orders_record["status"].append(i["status"])

    def playerIC_to_csv(self):
        """
        Write the player IC to a CSV file.
        """
        df = pd.DataFrame({ key:pd.Series(value) for key, value in self.playersIC.items() })
        df.to_csv(r"C:\Users\24395\Designated_Market_Making\output\playersIC.csv")

    def matched_to_csv(self):
        """
        Write the matched orders to a CSV file.
        """
        df = pd.DataFrame({ key:pd.Series(value) for key, value in self.matched_orders_record.items() })
        df.to_csv(r"C:\Users\24395\Designated_Market_Making\output\matched_orders.csv")

    def allorders_to_csv(self):
        """
        Write all the orders to a CSV file.
        """
        df = pd.DataFrame({ key:pd.Series(value) for key, value in self.all_orders_record.items() })
        df.to_csv(r"C:\Users\24395\Designated_Market_Making\output\all_orders.csv")

    def liquidity_to_csv(self):
        """
        Write the liquidity to a CSV file.
        """
        df = pd.DataFrame({ key:pd.Series(value) for key, value in self.liquidity.items() })
        df.to_csv(r"C:\Users\24395\Designated_Market_Making\output\liquidity.csv")

    def send_book(self):
        """
        Send the order book to the market maker.
        """
        self.mm_orderbook = []
        for i in self.mm_list:
            i.general_update(self.matched_orders, self.unsettled_orders, self.tickers, self.current_time)
            self.mm_orderbook.extend(i.trading_strategy())
        random.shuffle(self.mm_orderbook)

    def record_allplayers(self):
        """
        Record all the players if the current time is greater than or equal to the number of rounds.
        """
        if self.current_time >= self.num_rounds:
            self.playerIC_to_csv()
            self.matched_to_csv()
            self.allorders_to_csv()
            self.liquidity_to_csv()
