class Order:
    def __init__(self, order_id, customer_id, order_time, asset, order_type, order_price, order_quantity):
        """
        Initialize the Order class with the given parameters.

        Parameters:
        order_id (str): The unique identifier for the order.
        customer_id (str): The unique identifier for the customer.
        order_time (int): The time the order was placed.
        asset (str): The asset to be traded.
        order_type (str): The type of order ('BUY' or 'SELL').
        order_price (float): The price of the order.
        order_quantity (int): The quantity of the order.
        """
        self.order_id = order_id
        self.customer_id = customer_id
        self.order_time = order_time
        self.asset = asset
        self.order_type = order_type # 'BUY' or 'SELL'
        self.order_price = order_price
        self.order_quantity = order_quantity
        self.total_amount = order_price * order_quantity
        self.status = 'PENDING'

    def __str__(self):
        """
        Return a string representation of the Order.

        Returns:
        str: A string representation of the Order.
        """
        return f"Order ID: {self.order_id}, Customer ID: {self.customer_id}, Order Time: {self.order_time}, Order Type: {self.order_type}, Order Price: {self.order_price}, Order Quantity: {self.order_quantity}, Total Amount: {self.total_amount}"

    def __dict__(self):
        """
        Return a dictionary representation of the Order.

        Returns:
        dict: A dictionary representation of the Order.
        """
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "order_time": self.order_time,
            "asset": self.asset,
            "order_type": self.order_type,
            "order_price": self.order_price,
            "order_quantity": self.order_quantity,
            "total_amount": self.total_amount,
            "status": self.status
        }

    def getcustomerid(self):
        """
        Get the customer ID of the Order.

        Returns:
        str: The customer ID of the Order.
        """
        return self.customer_id

    def getorderid(self):
        """
        Get the order ID of the Order.

        Returns:
        str: The order ID of the Order.
        """
        return self.order_id

    def getordertime(self):
        """
        Get the order time of the Order.

        Returns:
        int: The order time of the Order.
        """
        return self.order_time

    def getasset(self):
        """
        Get the asset of the Order.

        Returns:
        str: The asset of the Order.
        """
        return self.asset

    def getordertype(self):
        """
        Get the order type of the Order.

        Returns:
        str: The order type of the Order.
        """
        return self.order_type

    def getorderprice(self):
        """
        Get the order price of the Order.

        Returns:
        float: The order price of the Order.
        """
        return self.order_price

    def getorderquantity(self):
        """
        Get the order quantity of the Order.

        Returns:
        int: The order quantity of the Order.
        """
        return self.order_quantity

    def gettotalamount(self):
        """
        Get the total amount of the Order.

        Returns:
        float: The total amount of the Order.
        """
        return self.total_amount

    def getstatus(self):
        """
        Get the status of the Order.

        Returns:
        str: The status of the Order.
        """
        return self.status

    def setstatus(self,status):
        """
        Set the status of the Order.

        Parameters:
        status (str): The new status of the Order ('PENDING', 'EXECUTED', 'CANCELLED').
        """
        self.status = status