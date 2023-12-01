import pandas as pd
import numpy as np
import src.browniance_motion as bm

class price_simulate:
    def __init__(self,MarketPath = None) -> None:
        self.marketdf = pd.read_csv(MarketPath,nrows=10000) if MarketPath != None else print("Generate simulate market")
        self.timestamp = 0
        self.volatility = 0.3
        self.steps = 100
        self.spread = 0.05
        self.market = bm.Brownian(volatility=self.volatility,steps=self.steps)
    
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
            orderbook['ask1_price'] = price+spread/2
            orderbook['ask1_quantity'] = np.random.choice([1,2,3])
            orderbook['bid1_price'] = price-spread/2
            orderbook['bid1_quantity'] = np.random.choice([1,2,3])       
        return orderbook
