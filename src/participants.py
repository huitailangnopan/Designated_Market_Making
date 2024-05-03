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
        self.midprice_list = []
        self.midprice = 0

    def update_time(self, current_time):
        self.current_time = current_time

    def update_tickers(self, tickers):
        self.tickers = tickers

    def update_midprice(self, midprice):
        self.midprice = midprice

    def receive_feedback(self, feedback, id):
        self.update_inventory(feedback, id)

    def eagleeye(self, future_price):
        self.future_price = future_price

    def trading_strategy(self):
        self.orders = []
        if self.current_time == 0:
            return self.orders
        if self.midprice != 0:
            self.midprice_list.append(self.midprice)
        # if len(self.midprice_list) >= 1:
        #     self.future_price[self.current_time - 1] = self.midprice_list[-1]
        five_steps_later = self.future_price[self.current_time + 4]
        profit_margin = abs(five_steps_later - self.future_price[self.current_time - 1])
        if five_steps_later > self.future_price[self.current_time - 1]:
            bid_price = min(round(self.future_price[self.current_time - 1] + 0.05 * profit_margin, 2), round(self.midprice * 1.02, 2)) if self.midprice != 0 else round(self.future_price[self.current_time - 1] + 0.05 * profit_margin, 2)
            bid_quantity = min(max(self.max_tolerance - self.inventory, 0),5)
            if bid_quantity > 0 and five_steps_later > self.midprice * 0.9:
                self.orders.append(self.generate_marketorder(-1, 'BUY', bid_price, bid_quantity))
        else:
            ask_price = min(round(self.future_price[self.current_time - 1] - 0.05 * profit_margin, 2), round(self.midprice * 1.03, 2)) if self.midprice != 0 else round(self.future_price[self.current_time - 1] - 0.05 * profit_margin, 2)
            ask_quantity = min(max(self.max_tolerance + self.inventory, 0),5)
            if ask_quantity > 0 and five_steps_later < self.midprice * 1.1:
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
    # Participant 2 represents a bunch of people, not just one person
    def __init__(self):
        self.tickers = None
        self.current_time = 0
        self.orders = []
        self.prev_price = []
        self.prev_order = []
        self.inventory = 0
        self.inventory_history = []
        self.asset = "IBM"
        self.wish_to_liquidate = 10
        self.cash_history = []
        self.matched_trades = []
        self.unsettled_orders = []
        self.midprice = 0

    def update_time(self, current_time):
        self.current_time = current_time

    def update_midprice(self, midprice):
        self.midprice = midprice

    def update_tickers(self, tickers):
        self.tickers = tickers

    def receive_feedback(self, matched_trades,unsettled_trades):
        self.matched_trades = matched_trades
        self.unsettled_orders = unsettled_trades

    def trading_strategy(self):
        self.orders = []
        if len(self.unsettled_orders) == 0 and len(self.matched_trades) == 0:
            return self.orders
        if len(self.unsettled_orders) > 0:
            buy_orders = [order.getorderprice() for order in self.unsettled_orders if order.getordertype() == 'BUY']
            sell_orders = [order.getorderprice() for order in self.unsettled_orders if order.getordertype() == 'SELL']
            if len(buy_orders) > 0:
                sell_price = max(buy_orders)
                self.orders.append(self.generate_marketorder(-2, 'SELL', sell_price, self.wish_to_liquidate))
            else:
                if len(self.matched_trades) > 0:
                    sell_orders = [order["Matched Price"] for order in self.matched_trades]
                    if len(buy_orders) > 0:
                        buy_price = min(buy_orders)
                        self.orders.append(self.generate_marketorder(-2, 'BUY', buy_price, self.wish_to_liquidate))
            if len(sell_orders) > 0:
                buy_price = min(sell_orders)
                self.orders.append(self.generate_marketorder(-2, 'BUY', buy_price, self.wish_to_liquidate))
            else:
                if len(self.matched_trades) > 0:
                    sell_orders = [order["Matched Price"] for order in self.matched_trades]
                    if len(sell_orders) > 0:
                        sell_price = max(sell_orders)
                        self.orders.append(self.generate_marketorder(-2, 'SELL', sell_price, self.wish_to_liquidate))
        self.prev_order = self.orders
        return self.orders

    def generate_marketorder(self, customer_id, order_type, order_price, order_quantity):
        order_id = str(self.current_time) + str(self.asset) + str(random.randint(0, 100))
        customer_id = customer_id
        order_time = self.current_time
        return Order(order_id, customer_id, order_time, self.asset, order_type, order_price, order_quantity)



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
        self.max_tolerance = 50
        self.cash = 100
        self.cash_history = []
        self.midprice_list = []
        self.midprice = 0

    def update_time(self, current_time):
        self.current_time = current_time

    def update_tickers(self, tickers):
        self.tickers = tickers

    def update_midprice(self, midprice):
        self.midprice = midprice

    def receive_feedback(self, feedback, id):
        self.update_inventory(feedback, id)

    def eagleeye(self, prev_price):
        self.prev_price = prev_price

    def trading_strategy(self):
        self.orders = []
        if self.current_time in (0, 1):
            return self.orders
        else:
            if self.midprice != 0:
                self.midprice_list.append(self.midprice)
            # if len(self.midprice_list) >= 1:
            #     self.prev_price[self.current_time - 2] = self.midprice_list[-1]
            expected_growth = self.prev_price[self.current_time - 1] - self.prev_price[self.current_time - 2]
            profit_margin = abs(self.prev_price[self.current_time - 1] - self.prev_price[self.current_time - 2])
            if expected_growth > 0:
                bid_price = min(round(self.prev_price[self.current_time - 1] + 0.05 * profit_margin, 2), round(self.midprice * 1.02, 2)) if self.midprice != 0 else round(self.prev_price[self.current_time - 1] + 0.05 * profit_margin, 2)
                bid_quantity = min(max(self.max_tolerance - self.inventory, 0), 10)
                if bid_quantity > 0 and self.prev_price[self.current_time - 1] > self.midprice * 0.9:
                    self.orders.append(self.generate_marketorder(-3, 'BUY', bid_price, bid_quantity))
            else:
                ask_price = min(round(self.prev_price[self.current_time - 1] - 0.05 * profit_margin, 2), round(self.midprice * 1.03, 2)) if self.midprice != 0 else round(self.prev_price[self.current_time - 1] - 0.05 * profit_margin, 2)
                ask_quantity = min(max(self.max_tolerance + self.inventory, 0), 10)
                if ask_quantity > 0 and self.prev_price[self.current_time - 1] < self.midprice * 1.1:
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