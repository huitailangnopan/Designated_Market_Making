
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
        orders = self.mm_orderbook.copy()
        orders.extend(self.marketorder)
        matched = []
        buy_orders = [order for order in orders if order.getordertype() == 'BUY' and order.getstatus() != 'EXECUTED']
        sell_orders = [order for order in orders if order.getordertype() == 'SELL' and order.getstatus() != 'EXECUTED']
        matches_found = True

        while matches_found:
            matches_found = False  # Assume no matches at the start of each iteration
            for buy_order in buy_orders:
                for sell_order in sell_orders:
                    if buy_order.getstatus() == 'EXECUTED' or sell_order.getstatus() == 'EXECUTED':
                        continue  # Skip already executed orders

                    if buy_order.getasset() == sell_order.getasset() and buy_order.getorderprice() >= sell_order.getorderprice():
                        # Determine matched quantity and price
                        matched_quantity = min(buy_order.getorderquantity(), sell_order.getorderquantity())
                        matched_price = min(buy_order.getorderprice(), sell_order.getorderprice())

                        # Update orders based on the matched quantity
                        buy_order.order_quantity -= matched_quantity
                        sell_order.order_quantity -= matched_quantity

                        if buy_order.getorderquantity() == 0:
                            buy_order.setstatus('EXECUTED')
                        if sell_order.getorderquantity() == 0:
                            sell_order.setstatus('EXECUTED')

                        # Record the match
                        matched.append({
                            "Time": self.current_time,
                            "Matched Price": matched_price,
                            "Matched Quantity": matched_quantity,
                            "Buyer": buy_order.getcustomerid(),
                            "Seller": sell_order.getcustomerid()
                        })

                        print(f"Time: {self.current_time}, Matched Price: {matched_price}, "
                              f"Quantity: {matched_quantity}, Buyer: {buy_order.getcustomerid()}, "
                              f"Seller: {sell_order.getcustomerid()}")

                        matches_found = True  # Indicate that a match was found in this iteration

                        if buy_order.getstatus() == 'EXECUTED' or sell_order.getstatus() == 'EXECUTED':
                            break  # Move on to the next buy order if one of the orders was fully executed

                # Refresh the lists to remove executed orders for the next iteration
                buy_orders = [order for order in buy_orders if order.getstatus() != 'EXECUTED']
                sell_orders = [order for order in sell_orders if order.getstatus() != 'EXECUTED']
        return matched,orders

"""
    def exchange_execute(self):
        orders = self.mm_orderbook.copy()
        orders.extend(self.marketorder)
        matched = []
        for order in orders:
            if order.getstatus() == 'EXECUTED':
                continue
            for match_order in orders:
                if match_order.getstatus() == 'EXECUTED':
                    continue
                if order.getstatus() == 'EXECUTED':
                    break
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


"""


    