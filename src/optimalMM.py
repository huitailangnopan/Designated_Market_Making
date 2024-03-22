import pandas as pd
import numpy as np
from src.utils import order_process
import os
from src.order import Order
import random


class marketmarker:
    def __init__(self):
        self.tickers = None
        self.current_time = 0
        self.orders = []
        self.prev_price = []
        self.prev_order = []
        self.inventory = 0
        self.inventory_history = []
        self.asset = "IBM"
        self.max_tolerance = 100
        self.cash = 100
        self.cash_history = []
        self.id = 1

    def update_time(self, current_time):
        self.current_time = current_time

    def update_tickers(self, tickers):
        self.tickers = tickers

    def receive_feedback(self, feedback):
        self.update_inventory(feedback)

    def general_update(self, feedback, tickers, time):
        self.update_tickers(tickers)
        self.update_time(time)
        self.receive_feedback(feedback)

    def update_inventory(self, matched):
        for i in matched:
            if i["Buyer"] == self.id:
                self.inventory += i["Matched Quantity"]
                self.cash -= i["Matched Quantity"] * i["Matched Price"]
            elif i["Seller"] == self.id:
                self.inventory -= i["Matched Quantity"]
                self.cash += i["Matched Quantity"] * i["Matched Price"]
        self.inventory_history.append(self.inventory)
        self.cash_history.append(self.cash)

    def trading_strategy(self, current_time, latest_orderbook, mm_no):
        myorder = []
        orderbook = {}
        orderbook["ask_prices"] = []
        orderbook["bid_prices"] = []
        orderbook["ask_quantity"] = []
        orderbook['bid_quantity'] = []
        asset = "IBM"
        for i in latest_orderbook:
            if i.getordertype() == "SELL":
                orderbook["ask_prices"].append(i.getorderprice())
                orderbook["ask_quantity"].append(i.getorderquantity())
            if i.getordertype() == "BUY":
                orderbook["bid_prices"].append(i.getorderprice())
                orderbook["bid_quantity"].append(i.getorderquantity())
        if len(orderbook['ask_quantity']) + len(orderbook['bid_quantity']) != 0:
            possible_addon = 0
            mid_price = (sum(orderbook["bid_prices"]) + sum(orderbook["ask_prices"]))/(len(orderbook['ask_quantity'])+len(orderbook['bid_quantity']))
            for i in range(len(orderbook['ask_prices'])):
                bid_price = orderbook['ask_prices'][i]
                bid_quantity = orderbook['ask_quantity'][i]
                if bid_quantity+possible_addon+self.inventory < self.max_tolerance:
                    myorder.append(self.generate_marketorder(current_time, asset, "BUY", bid_price, bid_quantity, mm_no))
                    possible_addon += bid_quantity
            for i in range(len(orderbook['bid_prices'])):
                ask_price = orderbook['bid_prices'][i]
                ask_quantity = orderbook['bid_quantity'][i]
                if ask_quantity - possible_addon - self.inventory < self.max_tolerance:
                    myorder.append(self.generate_marketorder(current_time, asset, "SELL", ask_price, ask_quantity, mm_no))
                    possible_addon -= ask_quantity
            if self.inventory > self.max_tolerance * 0.7:
                sell_quantity = int(self.inventory - self.max_tolerance * 0.7)
                myorder.append(self.generate_marketorder(current_time, asset, "SELL",mid_price, sell_quantity, mm_no))
            if self.inventory < -1 * self.max_tolerance * 0.7:
                buy_quantity = int(-1 * self.inventory - self.max_tolerance * 0.7)
                myorder.append(self.generate_marketorder(current_time, asset, "BUY", mid_price, buy_quantity, mm_no))
        return myorder

    def generate_marketorder(self, current_time, asset, order_type, order_price, order_quantity, mm_no):
        order_id = str(current_time) + str(asset) + str(random.randint(0, 100))
        customer_id = mm_no
        order_time = current_time
        return Order(order_id, customer_id, order_time, asset, order_type, order_price, order_quantity)
