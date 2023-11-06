from django.db import models
from .mixin import TimestampMixin


class MenuCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image_url = models.CharField(max_length=200)
    disabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Menu(TimestampMixin, models.Model):
    item_name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.PositiveIntegerField()
    category = models.ForeignKey(
        MenuCategory, on_delete=models.SET_NULL, blank=True, null=True
    )
    is_vegetarian = models.BooleanField(default=False)
    is_spicy = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "item_name",
                ],
                name="item_name_idx",
            ),
            models.Index(fields=["category"], name="category_idx"),
        ]

    def __str__(self):
        return self.item_name
