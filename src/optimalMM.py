import pandas as pd
import numpy as np
from src.utils import order_process

def trading_strategy(current_time):
    orderbook = order_process.read(current_time)
    ask1_price = orderbook['ask1_price']
    ask1_quantity = orderbook['ask1_quantity']
    bid1_price = orderbook['bid1_price']
    bid1_quantity = orderbook['bid1_quantity']
    fair_price = (ask1_price*ask1_quantity + bid1_price*bid1_quantity)/2
    myorder = {}
    myorder['ask1_price'] = fair_price+1
    myorder['ask1_quantity'] = 1
    myorder['bid1_price'] = fair_price-1
    myorder['bid1_quantity'] = 1
    myorder = {'IBM':myorder}
    order_process.submit(current_time,myorder)


    
    