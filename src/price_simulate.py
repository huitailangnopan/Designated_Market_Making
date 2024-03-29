import pandas as pd
import numpy as np
import src.browniance_motion as bm
from scipy.stats import poisson
import random
from src.order import Order
from src.participants import Participant1, Participant2, Participant3


class PriceSimulator:
    def __init__(self, MarketPath=None):
        self.marketdf = pd.read_csv(MarketPath, nrows=10000) if MarketPath else print("Generate simulate market")
        self.timestamp = 0
        self.volatility = 0.25
        self.steps = 4000
        self.spread = 0.05
        self.num_sim = 5
        self.p_start = 134
        self.asset = 'IBM'
        self.market = bm.Brownian(volatility=self.volatility, steps=self.steps, num=self.num_sim, p_start=self.p_start)
        self.orderbook = []
        self.orderbook_returnedbyexhcange = []
        self.matched_orders = []
        self.p1 = Participant1()
        self.p3 = Participant3()

    def load_market(self, MarketPath):
        self.marketdf = pd.read_csv(MarketPath, nrows=10000)

    def next_time(self):
        self.timestamp += 1
        self.reset_orderbook()

    def reset_orderbook(self):
        self.orderbook = []

    def updatebook(self, order):
        if type(order) is list:
            for i in order:
                self.orderbook.append(i)
        else:
            self.orderbook.append(order)

    def updatedOrderbookfromExchange(self, matched_orders):
        self.orderbook_returnedbyexhcange = matched_orders

    def get_newest_orderbook(self, real_mkt=False, asset='IBM'):
        self.asset = asset
        self.next_time()
        if real_mkt:
            temp = self.marketdf.iloc[self.timestamp:self.timestamp + 1]
            ask_price = round(float(temp.iloc[0, 4]), 2)
            ask_quantity = int(temp.iloc[0, 5])
            bid_price = round(float(temp.iloc[0, 2]), 2)
            bid_quantity = int(temp.iloc[0, 3])
            buy_order = self.generate_marketorder('BUY', bid_price, bid_quantity)
            sell_order = self.generate_marketorder('SELL', ask_price, ask_quantity)
            self.updatebook(buy_order)
            self.updatebook(sell_order)
        else:
            for i in range(random.randint(0, 5)):
                price = self.market[0][self.timestamp]
                spread = s = np.random.lognormal(-1.6, 0.5, 20)[0]
                # p_order = poisson.pmf(k=1, mu=0.7)
                # if random.uniform(0, 1) >= p_order:
                ask_price = round(price + spread / 2, 1)
                ask_quantity = random.randint(1, 5)
                self.updatebook(self.generate_marketorder('SELL', ask_price, ask_quantity))
            for i in range(random.randint(0, 5)):
                price = self.market[0][self.timestamp]
                spread = s = np.random.lognormal(-1.6, 0.5, 20)[0]
                bid_price = round(price - spread / 2, 1)
                bid_quantity = random.randint(1, 5)
                self.updatebook(self.generate_marketorder('BUY', bid_price, bid_quantity))
        self.get_order_marketparticipants()
        return self.orderbook

    def generate_marketorder(self, order_type, order_price, order_quantity):
        order_id = str(self.timestamp) + str(self.asset) + str(random.randint(0, 100))
        customer_id = 0
        order_time = self.timestamp
        return Order(order_id, customer_id, order_time, self.asset, order_type, order_price, order_quantity)

    def init_participants(self):
        self.p1.update_time(self.timestamp)
        self.p1.update_tickers(self.asset)
        self.p1.eagleeye(self.market[0])
        self.p3.update_time(self.timestamp)
        self.p3.update_tickers(self.asset)
        self.p3.eagleeye(self.market[0])

    def get_order_marketparticipants(self):
        self.init_participants()
        self.p1.receive_feedback(self.orderbook_returnedbyexhcange, -1)
        self.p3.receive_feedback(self.orderbook_returnedbyexhcange, -3)
        self.updatebook(self.p1.trading_strategy())
        self.updatebook(self.p3.trading_strategy())

    def record_participants(self):
        return self.p1.inventory_history, self.p1.cash_history, self.p3.inventory_history, self.p3.cash_history
