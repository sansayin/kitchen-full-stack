from order_service.models import Menu, MenuCategory
from ninja import ModelSchema


class MenuItemOut(ModelSchema):
    class Config:
        model = Menu
        model_fields = ["id", "item_name", "price", "image_url", "category"]


class MenuCategoryOut(ModelSchema):
    class Config:
        model = MenuCategory
        model_fields = "__all__"
