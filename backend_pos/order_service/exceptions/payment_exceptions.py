class NotPaidException(Exception):
    def __init__(self, message="Order Not Paid Yet"):
        self.message = message
        super().__init__(self.message)


class InvalidCreditCardException(Exception):
    def __init__(self, message="Credit Card not valid"):
        self.message = message
        super().__init__(self.message)
