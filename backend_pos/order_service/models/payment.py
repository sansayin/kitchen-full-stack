from django.db import models
from .mixin import TimestampMixin

from django.db import models


class Payment(TimestampMixin, models.Model):
    order_id = models.CharField(max_length=50)
    amount = models.PositiveIntegerField(null=False)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"Payment ID: {self.pk}, Amount: {self.amount} {self.currency}, Status: {self.status}"
