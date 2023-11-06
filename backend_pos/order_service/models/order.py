from django.db import models
from .mixin import TimestampMixin


class Order(TimestampMixin, models.Model):
    order_id = models.CharField(max_length=64)
    meal_id = models.PositiveIntegerField()
    item_name = models.CharField(max_length=100)
    total_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    done = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "meal_id",
                ],
                name="meal_idx",
            )
        ]

    def __str__(self):
        return self.item_name
