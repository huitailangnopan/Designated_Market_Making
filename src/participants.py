from src.order import Order
import random
class Participant1:
    def __init__(self, tickers, future_price):
        self.tickers = tickers
        self.future_price = future_price
        self.current_time = 0
        self.orders = []
        self.prev_order = []
        self.inventory = 0
        self.asset = "IBM"
        self.max_tolerance = 20

    def update_time(self, current_time):
        self.current_time = current_time

    def receive_feedback(self, feedback):
        pass

    def eagleeye(self, future_price):
        self.future_price = future_price

    def trading_strategy(self):
        five_steps_later = self.future_price[self.current_time + 5]
        profit_margin = abs(five_steps_later - self.future_price[self.current_time])
        if five_steps_later > self.future_price[self.current_time]:
            bid_price = self.future_price[self.current_time] + 0.05*profit_margin
            self.orders.append(self.generate_marketorder(-1,'BUY', self.future_price[self.current_time] + 1, self.max_tolerance-self.inventory))
        else:
            ask_price = self.future_price[self.current_time] - 0.05*profit_margin
            self.orders.append(self.generate_marketorder(-1,'SELL', self.future_price[self.current_time] - 1, self.max_tolerance+self.inventory))
        self.prev_order = self.orders
        return self.orders

    def generate_marketorder(self, customer_id, order_type, order_price, order_quantity):
        order_id = str(self.current_time)+str(self.asset)+str(random.randint(0, 100))
        customer_id = customer_id
        order_time = self.current_time
        return Order(order_id, customer_id, order_time, self.asset, order_type, order_price, order_quantity)


class Participant2:
    pass


class Participant3:
    pass
