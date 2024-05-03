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
        self.unsettled_orders = []
        self.matched_orders = []
        self.p1 = Participant1()
        self.p2 = Participant2()
        self.p3 = Participant3()
        self.mid_price = 0
        self.shock = False

    def get_fundamental_value(self):
        return self.market[0]

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

    def updatedOrderbookfromExchange(self, matched_orders,unsettled_orders):
        self.orderbook_returnedbyexhcange = matched_orders
        self.unsettled_orders = unsettled_orders

    def get_newest_orderbook(self, real_mkt=False, asset='IBM'):
        self.asset = asset
        self.next_time()
        latest_orderbook = self.unsettled_orders
        orderbook = {}
        orderbook["ask_prices"] = []
        orderbook["bid_prices"] = []
        orderbook["ask_quantity"] = []
        orderbook['bid_quantity'] = []
        for i in latest_orderbook:
            if i.getordertype() == "SELL" and i.getcustomerid() <= 0:
                orderbook["ask_prices"].append(i.getorderprice())
                orderbook["ask_quantity"].append(i.getorderquantity())
            if i.getordertype() == "BUY" and i.getcustomerid() <= 0:
                orderbook["bid_prices"].append(i.getorderprice())
                orderbook["bid_quantity"].append(i.getorderquantity())
        if sum(orderbook['ask_quantity']) + sum(orderbook['bid_quantity']) != 0:
            mid_price = (np.dot(orderbook["bid_prices"], orderbook["bid_quantity"]) + np.dot(orderbook["ask_prices"], orderbook["ask_quantity"])) / (sum(orderbook['ask_quantity']) + sum(orderbook['bid_quantity']))
            mid_price = round(mid_price, 2)
        else:
            mid_price = 0
        self.mid_price = mid_price
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
            if self.shock:
                if self.timestamp == 500:
                    y = [k*1.3 for k in self.market[0][500:]]
                    self.market[0][500:] = y
            if self.market[0][self.timestamp] < mid_price*1.1:
                for i in range(random.randint(0, 5)):
                    price = self.market[0][self.timestamp]
                    spread = s = np.random.lognormal(-1.6, 0.5, 20)[0]
                    # p_order = poisson.pmf(k=1, mu=0.7)
                    # if random.uniform(0, 1) >= p_order:
                    ask_price = min(round(price + spread / 2, 1), round(mid_price * 1.03, 2)) if mid_price != 0 else round(price + spread / 2, 1)
                    ask_quantity = random.randint(1, 10)
                    self.updatebook(self.generate_marketorder('SELL', ask_price, ask_quantity))
            if self.market[0][self.timestamp] > mid_price*0.9:
                for i in range(random.randint(0, 5)):
                    price = self.market[0][self.timestamp]
                    spread = s = np.random.lognormal(-1.6, 0.5, 20)[0]
                    bid_price = min(round(price - spread / 2, 1), round(mid_price * 1.02, 2)) if mid_price != 0 else round(price + spread / 2, 1)
                    bid_quantity = random.randint(1, 10)
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
        self.p1.update_midprice(self.mid_price)
        self.p2.update_time(self.timestamp)
        self.p2.update_tickers(self.asset)
        self.p2.update_midprice(self.mid_price)
        self.p3.update_time(self.timestamp)
        self.p3.update_tickers(self.asset)
        self.p3.eagleeye(self.market[0])
        self.p3.update_midprice(self.mid_price)

    def get_order_marketparticipants(self):
        self.init_participants()
        self.p1.receive_feedback(self.orderbook_returnedbyexhcange, -1)
        self.p2.receive_feedback(self.orderbook_returnedbyexhcange, self.unsettled_orders)
        self.p3.receive_feedback(self.orderbook_returnedbyexhcange, -3)
        self.updatebook(self.p1.trading_strategy())
        self.updatebook(self.p2.trading_strategy())
        self.updatebook(self.p3.trading_strategy())

    def record_participants(self):
        return self.p1.inventory_history, self.p1.cash_history, self.p3.inventory_history, self.p3.cash_history
