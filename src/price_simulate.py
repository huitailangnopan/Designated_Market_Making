import pandas as pd
import numpy as np
import src.browniance_motion as bm
from scipy.stats import poisson
import random

class price_simulate:
    def __init__(self,MarketPath = None) -> None:
        self.marketdf = pd.read_csv(MarketPath,nrows=10000) if MarketPath != None else print("Generate simulate market")
        self.timestamp = 0
        self.volatility = 0.3
        self.steps = 300
        self.spread = 0.05
        self.num_sim = 5
        self.p_start = 134
        self.market = bm.Brownian(volatility=self.volatility,steps=self.steps,num=self.num_sim,p_start=self.p_start)
    
    def LoadMarket(self,MarketPath) -> None:
        self.marketdf = pd.read_csv(MarketPath,nrows=10000)
    
    def next_time(self) -> None:
        self.timestamp = self.timestamp+1
    
    def get_newest_orderbook(self,real_mkt = True) -> dict:
        self.next_time()
        orderbook = {}
        if real_mkt:
            temp = self.marketdf.iloc[self.timestamp:self.timestamp+1]
            orderbook['ask1_price'] = float(temp.iloc[0,4])
            orderbook['ask1_quantity'] = int(temp.iloc[0,5])
            orderbook['bid1_price'] = float(temp.iloc[0,2])
            orderbook['bid1_quantity'] = int(temp.iloc[0,3])
        else:
            price = self.market[0][self.timestamp]
            dt = self.spread/self.steps
            spread = np.random.normal(0,np.sqrt(dt))
            p_order = poisson.pmf(k=1, mu=0.7)
            if random.uniform(0, 1)<p_order:
                orderbook['ask1_price'] = 0
                orderbook['ask1_quantity'] = 0
                orderbook['bid1_price'] = 0
                orderbook['bid1_quantity'] = 0
            else:
                orderbook['ask1_price'] = price+spread/2
                orderbook['ask1_quantity'] = np.random.choice([1,2,3])
                orderbook['bid1_price'] = price-spread/2
                orderbook['bid1_quantity'] = np.random.choice([1,2,3])
            #else:
            """
                orderbook['ask1_price'] = 0
                orderbook['ask1_quantity'] = 0
                orderbook['bid1_price'] = 0
                orderbook['bid1_quantity'] = 0
            """
        return orderbook
