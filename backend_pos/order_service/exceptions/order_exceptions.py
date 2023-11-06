class OrderException(Exception):
    def __init__(self, message="Can not process order, try later"):
        self.message = message
        super().__init__(self.message)
