import pandas as pd
import numpy as np
from src.utils import order_process
import os

def trading_strategy(current_time):
    orderbook = order_process.read(current_time)
    ask1_price = orderbook['ask1_price']
    ask1_quantity = orderbook['ask1_quantity']
    bid1_price = orderbook['bid1_price']
    bid1_quantity = orderbook['bid1_quantity']
    myorder = {}
    if ask1_quantity + bid1_quantity != 0:
        fair_price = (ask1_price * ask1_quantity + bid1_price * bid1_quantity) / (ask1_quantity + bid1_quantity)
        myorder['ask1_price'] = fair_price+1
        myorder['ask1_quantity'] = ask1_quantity
        myorder['bid1_price'] = fair_price-1
        myorder['bid1_quantity'] = bid1_quantity
    else:
        myorder['ask1_price']=myorder['ask1_quantity']=myorder['bid1_price']=myorder['bid1_quantity']=0
    myorder = {'IBM':myorder}
    order_process.submit(current_time,myorder)

