from src.order import Order
import random


class Participant1:
    def __init__(self):
        self.tickers = None
        self.future_price = []
        self.current_time = 0
        self.orders = []
        self.prev_order = []
        self.inventory = 0
        self.inventory_history = []
        self.asset = "IBM"
        self.max_tolerance = 25
        self.cash = 100
        self.cash_history = []

    def update_time(self, current_time):
        self.current_time = current_time

    def update_tickers(self, tickers):
        self.tickers = tickers

    def receive_feedback(self, feedback, id):
        self.update_inventory(feedback, id)

    def eagleeye(self, future_price):
        self.future_price = future_price

    def trading_strategy(self):
        self.orders = []
        if self.current_time == 0:
            return self.orders
        five_steps_later = self.future_price[self.current_time + 4]
        profit_margin = abs(five_steps_later - self.future_price[self.current_time - 1])
        if five_steps_later > self.future_price[self.current_time - 1]:
            bid_price = round(self.future_price[self.current_time] + 0.05 * profit_margin, 2)
            bid_quantity = min(max(self.max_tolerance - self.inventory, 0),5)
            if bid_quantity > 0:
                self.orders.append(self.generate_marketorder(-1, 'BUY', bid_price, bid_quantity))
        else:
            ask_price = round(self.future_price[self.current_time - 1] - 0.05 * profit_margin, 2)
            ask_quantity = min(max(self.max_tolerance + self.inventory, 0),5)
            if ask_quantity > 0:
                self.orders.append(self.generate_marketorder(-1, 'SELL', ask_price, ask_quantity))
        self.prev_order = self.orders
        return self.orders

    def generate_marketorder(self, customer_id, order_type, order_price, order_quantity):
        order_id = str(self.current_time) + str(self.asset) + str(random.randint(0, 100))
        customer_id = customer_id
        order_time = self.current_time
        return Order(order_id, customer_id, order_time, self.asset, order_type, order_price, order_quantity)

    def update_inventory(self, matched, id):
        for i in matched:
            if i["Buyer"] == id:
                self.inventory += i["Matched Quantity"]
                self.cash -= i["Matched Quantity"] * i["Matched Price"]
            elif i["Seller"] == id:
                self.inventory -= i["Matched Quantity"]
                self.cash += i["Matched Quantity"] * i["Matched Price"]
        self.inventory_history.append(self.inventory)
        self.cash_history.append(self.cash)
    def record_inventory(self):
        return self.inventory_history

    def record_cash(self):
        return self.cash_history

class Participant2:
    pass


class Participant3:
    def __init__(self):
        self.tickers = None
        self.current_time = 0
        self.orders = []
        self.prev_price = []
        self.prev_order = []
        self.inventory = 0
        self.inventory_history = []
        self.asset = "IBM"
        self.max_tolerance = 25
        self.cash = 100
        self.cash_history = []

    def update_time(self, current_time):
        self.current_time = current_time

    def update_tickers(self, tickers):
        self.tickers = tickers

    def receive_feedback(self, feedback, id):
        self.update_inventory(feedback, id)

    def eagleeye(self, prev_price):
        self.prev_price = prev_price

    def trading_strategy(self):
        self.orders = []
        if self.current_time in (0, 1):
            return self.orders
        else:
            expected_growth = self.prev_price[self.current_time - 1] - self.prev_price[self.current_time - 2]
            profit_margin = abs(self.prev_price[self.current_time - 1] - self.prev_price[self.current_time - 2])
            if expected_growth > 0:
                bid_price = round(self.prev_price[self.current_time - 1] + 0.05 * profit_margin, 2)
                bid_quantity = min(max(self.max_tolerance - self.inventory, 0), 5)
                if bid_quantity > 0:
                    self.orders.append(self.generate_marketorder(-3, 'BUY', bid_price, bid_quantity))
            else:
                ask_price = round(self.prev_price[self.current_time - 1] - 0.05 * profit_margin, 2)
                ask_quantity = min(max(self.max_tolerance + self.inventory, 0), 5)
                if ask_quantity > 0:
                    self.orders.append(self.generate_marketorder(-3, 'SELL', ask_price, ask_quantity))
            self.prev_order = self.orders
        return self.orders

    def generate_marketorder(self, customer_id, order_type, order_price, order_quantity):
        order_id = str(self.current_time) + str(self.asset) + str(random.randint(0, 100))
        customer_id = customer_id
        order_time = self.current_time
        return Order(order_id, customer_id, order_time, self.asset, order_type, order_price, order_quantity)

    def update_inventory(self, matched, id):
        for i in matched:
            if i["Buyer"] == id:
                self.inventory += i["Matched Quantity"]
                self.cash -= i["Matched Quantity"] * i["Matched Price"]
            elif i["Seller"] == id:
                self.inventory -= i["Matched Quantity"]
                self.cash += i["Matched Quantity"] * i["Matched Price"]
        self.inventory_history.append(self.inventory)
        self.cash_history.append(self.cash)

    def record_inventory(self):
        return self.inventory_history

    def record_cash(self):
        return self.cash_history