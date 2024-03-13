import pandas as pd
import numpy as np
from src.utils import order_process
import os
from src.order import Order
import random

def trading_strategy(current_time,latest_orderbook,mm_no):
    myorder = []
    orderbook = {}
    orderbook["ask_prices"] = []
    orderbook["bid_prices"] = []
    orderbook["ask_quantity"] = []
    orderbook['bid_quantity'] = []
    asset = "IBM"
    for i in latest_orderbook:
        if i.getordertype() == "SELL":
            orderbook["ask_prices"].append(i.getprice())
            orderbook["ask_quantity"].append(i.getorderquantity())
        if i.getordertype() == "BUY":
            orderbook["bid_prices"].append(i.getprice())
            orderbook["bid_quantity"].append(i.getorderquantity())
    if len(orderbook['ask_quantity']) + len(orderbook['bid_quantity']) != 0:
        ask1_price = orderbook['ask_price'][0]
        ask1_quantity = orderbook['ask_quantity'][0]
        bid1_price = orderbook['bid_price'][0]
        bid1_quantity = orderbook['bid_quantity'][0]
        fair_price = (ask1_price * ask1_quantity + bid1_price * bid1_quantity) / (ask1_quantity + bid1_quantity)
        sellorder1 = generate_marketorder(current_time,asset,"SELL",fair_price+1,ask1_quantity,mm_no)
        buyorder1 = generate_marketorder(current_time,asset,"BUY",fair_price-1,ask1_quantity,mm_no)
        myorder.append(sellorder1)
        myorder.append(buyorder1)
    return myorder


def generate_marketorder(current_time, asset, order_type, order_price, order_quantity,mm_no):
    order_id = str(current_time) + str(asset) + str(random.randint(0, 100))
    customer_id = mm_no
    order_time = current_time
    return Order(order_id, customer_id, order_time, asset, order_type, order_price, order_quantity)
