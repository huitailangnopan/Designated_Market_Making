class Order:
    def __init__(self, order_id, customer_id, order_time, order_type, order_price, order_quantity):
        self.order_id = order_id
        self.customer_id = customer_id
        self.order_time = order_time
        self.order_type = order_type # 'BUY' or 'SELL'
        self.order_price = order_price
        self.order_quantity = order_quantity
        self.total_amount = order_price * order_quantity
        self.status = 'PENDING'


    def __str__(self):
        return f"Order ID: {self.order_id}, Customer ID: {self.customer_id}, Order Time: {self.order_time}, Order Type: {self.order_type}, Order Price: {self.order_price}, Order Quantity: {self.order_quantity}, Total Amount: {self.total_amount}"

    def getcustomerid(self):
        return self.customer_id

    def getorderid(self):
        return self.order_id

    def getordertime(self):
        return self.order_time

    def getordertype(self):
        return self.order_type

    def getorderprice(self):
        return self.order_price

    def getorderquantity(self):
        return self.order_quantity

    def gettotalamount(self):
        return self.total_amount

    def getstatus(self):
        return self.status

    def setstatus(self,status):
        self.status = status  # 'PENDING', 'EXECUTED', 'CANCELLED'