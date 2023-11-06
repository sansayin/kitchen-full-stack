from ninja import ModelSchema
from order_service.models import Payment


class PaymentIn(ModelSchema):
    class Config:
        model = Payment
        model_fields = ["order_id", "amount", "currency", "status"]


class PaymentOut(ModelSchema):
    class Config:
        model = Payment
        model_fields = ["order_id", "amount", "currency", "status"]
