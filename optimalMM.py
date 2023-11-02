import pandas as pd
import numpy as np
from trade_agent import Agent

def trading_strategy():
    new_agent = Agent("IBM",1)
    new_agent.update_tradebook()
    new_agent.update_price()
    orderbook = new_agent.get_orderbook()
    
    