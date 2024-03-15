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
        self.max_tolerance = 20
        self.cash = 100
        self.cash_history = []

    def update_time(self, current_time):
        self.current_time = current_time

    def update_tickers(self, tickers):
        self.tickers = tickers

    def receive_feedback(self, feedback,id):
        self.update_inventory(feedback,id)

    def general_update(self, feedback,id,tickers,time):
        self.update_tickers(tickers)
        self.update_time(time)
        self.receive_feedback(feedback,id)

    def generate_marketorder(self, customer_id, order_type, order_price, order_quantity):
        order_id = str(self.current_time)+str(self.asset)+str(random.randint(0, 100))
        customer_id = customer_id
        order_time = self.current_time
        return Order(order_id, customer_id, order_time, self.asset, order_type, order_price, order_quantity)

    def update_inventory(self, matched,id):
        for i in matched:
            if i["Buyer"] == id:
                self.inventory += i["Quantity"]
                self.cash -= i["Quantity"] * i["Price"]
            elif i["Seller"] == id:
                self.inventory -= i["Quantity"]
                self.cash += i["Quantity"] * i["Price"]


    def trading_strategy(self,current_time,latest_orderbook,mm_no):
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
            ask1_price = min(orderbook['ask_prices'])
            ask1_quantity = max(orderbook['ask_quantity'])
            bid1_price = max(orderbook['bid_prices'])
            bid1_quantity = max(orderbook['bid_quantity'])
            fair_price = (ask1_price * ask1_quantity + bid1_price * bid1_quantity) / (ask1_quantity + bid1_quantity)
            sellorder1 = self.generate_marketorder(current_time,asset,"SELL",fair_price+1,ask1_quantity,mm_no)
            buyorder1 = self.generate_marketorder(current_time,asset,"BUY",fair_price-1,ask1_quantity,mm_no)
            myorder.append(sellorder1)
            myorder.append(buyorder1)
        return myorder


    def generate_marketorder(self,current_time, asset, order_type, order_price, order_quantity,mm_no):
        order_id = str(current_time) + str(asset) + str(random.randint(0, 100))
        customer_id = mm_no
        order_time = current_time
        return Order(order_id, customer_id, order_time, asset, order_type, order_price, order_quantity)
