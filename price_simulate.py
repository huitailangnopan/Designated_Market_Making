import pandas as pd
import numpy as np

class price_simulate:
    def __init__(self) -> None:
        self.marketdf = None
        self.timestamp = 0
    
    def LoadMarket(self,MarketPath) -> None:
        self.marketdf = pd.read_csv(MarketPath)
        
    def generatemarket(self):
        pass
    
    def get_newest_orderbook(self):
        temp = self.marketdf[self.timestamp]
        orderbook = {}
        orderbook['ask1_price'] = temp.iloc[0,4]
        orderbook['ask1_quantity'] = temp.iloc[0,5]
        orderbook['bid1_price'] = temp.iloc[0,2]
        orderbook['bid1_quantity'] = temp.iloc[0,3]
        return orderbook
