import pandas as pd
import numpy as np

class price_simulate:
    def __init__(self,MarketPath = r"C:\Users\24395\Downloads\khypqgaihormjri2_csv\ibm_millisecond.csv") -> None:
        self.marketdf = pd.read_csv(MarketPath,nrows=10000)
        self.timestamp = 0
    
    def LoadMarket(self,MarketPath) -> None:
        self.marketdf = pd.read_csv(MarketPath,nrows=10000)
        
    def generatemarket(self):
        pass
    
    def next_time(self) -> None:
        self.timestamp = self.timestamp+1
    
    def get_newest_orderbook(self) -> dict:
        self.next_time()
        temp = self.marketdf.iloc[self.timestamp:self.timestamp+1]
        orderbook = {}
        orderbook['ask1_price'] = float(temp.iloc[0,4])
        orderbook['ask1_quantity'] = int(temp.iloc[0,5])
        orderbook['bid1_price'] = float(temp.iloc[0,2])
        orderbook['bid1_quantity'] = int(temp.iloc[0,3])
        return orderbook
