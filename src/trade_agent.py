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
        self.matched_orders_record = {"Time":[],"Matched Price":[],"Matched Quantity":[],"Buyer":[],"Seller":[]}
        self.all_orders_record = {"order_id":[],"customer_id":[],"order_time":[],
                                  "asset":[],"order_type":[],"order_price":[],"order_quantity":[],"total_amount":[],"status":[]}
        self.all_orders_updated = []
        self.mm1 = marketmarker()

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
        self.price_bot.updatedOrderbookfromExchange(self.matched_orders)
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
        order_book = self.latest_orderbook
        price = self.calculate_price(order_book)
        self.update_db("price_his", price)
        self.price_history.append(price)

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

    def exchange_execution(self):
        """
        Execute the exchange.
        """
        self.exchange.load_market(self.latest_orderbook)
        self.exchange.load_trade(self.mm_orderbook)
        self.exchange.update_time(self.current_time)
        self.matched_orders, self.all_orders_updated = self.exchange.exchange_execute()
        self.record_matched_orders()
        self.record_all_orders()

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

    def send_book(self):
        """
        Send the order book to the market maker.
        """
        self.mm_orderbook = []
        self.mm1.general_update(self.matched_orders, self.tickers, self.current_time)
        self.mm_orderbook.extend(self.mm1.trading_strategy(self.current_time, self.latest_orderbook, 1))

    def record_allplayers(self):
        """
        Record all the players if the current time is greater than or equal to the number of rounds.
        """
        if self.current_time >= self.num_rounds:
            playersIC = {}
            playersIC["mm1_inventory"] = self.mm1.inventory_history
            playersIC["mm1_cash"] = self.mm1.cash_history
            playersIC["p1_inventory"], playersIC["p1_cash"], playersIC["p3_inventory"], playersIC["p3_cash"] = self.price_bot.record_participants()
            playersIC["price_history"] = self.price_history
            df = pd.DataFrame({ key:pd.Series(value) for key, value in playersIC.items() })
            df.to_csv(r"C:\Users\24395\Designated_Market_Making\output\playersIC.csv")
            self.matched_to_csv()
            self.allorders_to_csv()
