
import pandas as pd
import numpy as np
import src.browniance_motion as bm
from scipy.stats import poisson
import random

class PriceSimulator:
    def __init__(self, MarketPath=None):
        self.marketdf = pd.read_csv(MarketPath, nrows=10000) if MarketPath else print("Generate simulate market")
        self.timestamp = 0
        self.volatility = 0.3
        self.steps = 1000
        self.spread = 0.05
        self.num_sim = 5
        self.p_start = 134
        self.market = bm.Brownian(volatility=self.volatility, steps=self.steps, num=self.num_sim, p_start=self.p_start)
        self.orderbook = {'ask_price': [], 'ask_quantity': [], 'bid_price': [], 'bid_quantity': []}

    def load_market(self, MarketPath):
        self.marketdf = pd.read_csv(MarketPath, nrows=10000)

    def next_time(self):
        self.timestamp += 1
        self.reset_orderbook()

    def reset_orderbook(self):
        self.orderbook = {'ask_price': [], 'ask_quantity': [], 'bid_price': [], 'bid_quantity': []}

    def update_orderbook(self, ask_price, ask_quantity, bid_price, bid_quantity):
        self.orderbook['ask_price'].append(ask_price)
        self.orderbook['ask_quantity'].append(ask_quantity)
        self.orderbook['bid_price'].append(bid_price)
        self.orderbook['bid_quantity'].append(bid_quantity)

    def get_newest_orderbook(self, real_mkt=True):
        self.next_time()
        if real_mkt:
            temp = self.marketdf.iloc[self.timestamp:self.timestamp + 1]
            self.update_orderbook(round(float(temp.iloc[0, 4]), 2), int(temp.iloc[0, 5]), round(float(temp.iloc[0, 2]), 2), int(temp.iloc[0, 3]))
        else:
            for i in range(random.randint(0, 5)):
                price = self.market[0][self.timestamp]
                spread = s = np.random.lognormal(-1.6, 0.5, 20)[0]
                p_order = poisson.pmf(k=1, mu=0.7)
                if random.uniform(0, 1) >= p_order:
                    self.update_orderbook(round(price + spread / 2, 1), np.random.choice([1, 2, 3]), round(price - spread / 2, 1), np.random.choice([1, 2, 3]))
        return self.orderbook
