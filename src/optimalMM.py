import pandas as pd
import numpy as np
from src.utils import order_process
import os

def trading_strategy(current_time):
    orderbook = order_process.read(current_time)
    myorder = {}
    myorder['ask_price'] = myorder['ask_quantity'] = myorder['bid_price'] = myorder['bid_quantity'] = []
    if len(orderbook['ask_quantity']) + len(orderbook['bid_quantity']) != 0:
        ask1_price = orderbook['ask_price'][0]
        ask1_quantity = orderbook['ask_quantity'][0]
        bid1_price = orderbook['bid_price'][0]
        bid1_quantity = orderbook['bid_quantity'][0]
        fair_price = (ask1_price * ask1_quantity + bid1_price * bid1_quantity) / (ask1_quantity + bid1_quantity)
        myorder['ask_price'].append(fair_price+1)
        myorder['ask_quantity'].append(ask1_quantity)
        myorder['bid_price'].append(fair_price-1)
        myorder['bid_quantity'].append(bid1_quantity)
    myorder = {'IBM':myorder}
    order_process.submit(current_time,myorder)

"""
make price into one list and bid into another list
"""
