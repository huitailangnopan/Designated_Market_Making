
class exchange:
    def __int__(self,current_time,marketorder,mm_orderbook):
        """
        Initialize the exchange class with the given parameters.

        Parameters:
        current_time (int): The current time.
        marketorder (list): The market order book.
        mm_orderbook (list): The market maker order book.
        """
        self.current_time = None
        self.marketorder = None
        self.mm_orderbook = None
        self.asset = "IBM"

    def update_time(self,time):
        """
        Update the current time.

        Parameters:
        time (int): The new time.
        """
        self.current_time = time

    def load_assets(self, assets):
        """
        Load the assets.

        Parameters:
        assets (list): The assets to be loaded.
        """
        self.assets = assets

    def load_market(self,marketorder):
        """
        Load the market order book.

        Parameters:
        marketorder (list): The market order book to be loaded.
        """
        self.marketorder = marketorder

    def load_trade(self,mm_orderbook):
        """
        Load the market maker order book.

        Parameters:
        mm_orderbook (list): The market maker order book to be loaded.
        """
        self.mm_orderbook = mm_orderbook

    def exchange_execute(self):
        """
        Execute the exchange by matching the orders in the market order book and trade order book.

        Returns:
        list: The matched orders and the updated orders.
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
                            buyer = order.getcustomerid() if order.getordertype() == 'BUY' else match_order.getcustomerid()
                            seller = match_order.getcustomerid() if order.getordertype() == 'BUY' else order.getcustomerid()
                            matched_price = min(match_order.getorderprice(), order.getorderprice())
                            matched.append({"Time": self.current_time,
                                            "Matched Price": matched_price,
                                            "Matched Quantity": match_order.getorderquantity(),
                                            "Buyer": buyer,
                                            "Seller": seller})
                            print(f"Time: {self.current_time}, "
                                  f"Matched Price: {matched_price}, "
                                  f"Quantity: {match_order.getorderquantity()}, "
                                  f"Buyer: {buyer}, Seller: {seller}")
                        elif order.getorderquantity() < match_order.getorderquantity():
                            order.setstatus('EXECUTED')
                            match_order.setstatus('PENDING')
                            match_order.order_quantity = match_order.getorderquantity() - order.getorderquantity()
                            buyer = order.getcustomerid() if order.getordertype() == 'BUY' else match_order.getcustomerid()
                            seller = match_order.getcustomerid() if order.getordertype() == 'BUY' else order.getcustomerid()
                            matched_price = min(match_order.getorderprice(), order.getorderprice())
                            matched.append({"Time": self.current_time,
                                            "Matched Price": matched_price,
                                            "Matched Quantity": order.getorderquantity(),
                                            "Buyer": buyer,
                                            "Seller": seller})
                            print(f"Time: {self.current_time}, "
                                  f"Matched Price: {matched_price}, "
                                  f"Quantity: {order.getorderquantity()}, "
                                  f"Buyer: {buyer}, Seller: {seller}")
                        else:
                            order.setstatus('EXECUTED')
                            match_order.setstatus('EXECUTED')
                            buyer = order.getcustomerid() if order.getordertype() == 'BUY' else match_order.getcustomerid()
                            seller = match_order.getcustomerid() if order.getordertype() == 'BUY' else order.getcustomerid()
                            matched_price = min(match_order.getorderprice(), order.getorderprice())
                            matched.append({"Time": self.current_time,
                                            "Matched Price": matched_price,
                                            "Matched Quantity": match_order.getorderquantity(),
                                            "Buyer": buyer,
                                            "Seller": seller})
                            print(f"Time: {self.current_time}, "
                                  f"Matched Price: {matched_price}, "
                                  f"Quantity: {match_order.getorderquantity()}, "
                                  f"Buyer: {buyer}, Seller: {seller}")
        return matched,orders





    