import pandas as pd
import numpy as np

class price_simulate:
    def __init__(self) -> None:
        self.marketdf = None
    
    def LoadMarket(self,MarketPath) -> None:
        self.marketdf = pd.read_csv(MarketPath)
        
    def generatemarket(self):
        pass
