from ninja import ModelSchema, Schema
from order_service.models import Order


"""
interface Order {
    meal_id: number;
    item_name: string;
    total_price: number;
    quantity: number;
}
"""


class OrderIn(ModelSchema):
    class Config:
        model = Order
        model_fields = ["order_id", "meal_id", "item_name", "total_price", "quantity"]
