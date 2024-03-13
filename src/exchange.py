import pandas as pd
import numpy as np
from sqlitedict import SqliteDict
from src.utils.analysis import sql_to_list,sql_to_pd

class exchange:
    def __int__(self,current_time,marketorder,mm_orderbook):
        self.current_time = None
        self.marketorder = None
        self.mm_orderbook = None
        self.asset = "IBM"

    def update_time(self,time):
        self.current_time = time

    def load_assets(self, assets):
        self.assets = assets

    def load_market(self,marketorder):
        """
        change_todo: change the dict key from sql_to_pd to a column in df, add the time index as well
        """
        self.marketorder = marketorder

    def load_trade(self,mm_orderbook):
        self.mm_orderbook = mm_orderbook

    def exchange_execute(self):
        """
        match the orders in the market order book and trade order book
        """
        orders = self.marketorder.copy()
        orders.extend(self.mm_orderbook)
        matched = []
        for order in orders:
            if order.getstatus() == 'EXECUTED':
                continue
            for match_order in orders:
                if match_order.getstatus() == 'EXECUTED':
                    continue
                if order.getasset() == match_order.getasset() and order.getordertype() != match_order.getordertype():
                    if (order.getordertype() == 'BUY' and order.getorderprice() >= match_order.getorderprice()) or \
                       (order.getordertype() == 'SELL' and order.getorderprice() <= match_order.getorderprice()):
                        if order.getorderquantity() > match_order.getorderquantity():
                            order.setstatus('PENDING')
                            match_order.setstatus('EXECUTED')
                            order.order_quantity = order.getorderquantity() - match_order.getorderquantity()
                            matched.append({"Matched Price": match_order.getorderprice(), "Matched Quantity": match_order.getorderquantity()})
                            print(f"Matched Price: {match_order.getorderprice()}, Quantity: {match_order.getorderquantity()}")
                        elif order.getorderquantity() < match_order.getorderquantity():
                            order.setstatus('EXECUTED')
                            match_order.setstatus('PENDING')
                            match_order.order_quantity = match_order.getorderquantity() - order.getorderquantity()
                            matched.append({"Matched Price": order.getorderprice(), "Matched Quantity": order.getorderquantity()})
                            print(f"Matched Price: {order.getorderprice()}, Quantity: {order.getorderquantity()}")
                        else:
                            order.setstatus('EXECUTED')
                            match_order.setstatus('EXECUTED')
                            matched.append({"Matched Price": order.getorderprice(), "Matched Quantity": order.getorderquantity()})
                            print(f"Matched Price: {order.getorderprice()}, Quantity: {order.getorderquantity()}")
        return matched,orders





    