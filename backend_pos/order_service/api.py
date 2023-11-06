"""
Strategy:

    Query APIs:
        For GET requests, which are typically used to retrieve data from the server, 
        it makes sense to prioritize cached data over direct database queries. 
        Cached data can significantly improve the response time and reduce the load
        on the database server.
        Caching can be implemented using various tools and mechanisms, such as 
        in-memory caches (e.g., Redis)

    Mutate APIs:
        For POST requests, which are used for data modification and updates, it's 
        generally a good practice to perform database mutations directly to maintain
        data consistency.
        However, if the database operations are resource-intensive or time-consuming, 
        offloading these operations to background tasks like Celery tasks or message 
        queue (MQ) consumers can be a great idea. This approach allows the API to 
        respond quickly and delegates the time-consuming work to background processes
"""

import json
from typing import List
from billiard.util import functools
from django.core.cache import caches
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from ninja.security import django_auth
from ninja.errors import ValidationError
from ninja import NinjaAPI, Router, Schema
from order_service.models import Menu, MenuCategory, Payment
from order_service.schemas import (
    MenuItemOut,
    MenuCategoryOut,
    OrderIn,
    PaymentIn,
    PaymentOut,
)
from order_service.exceptions.payment_exceptions import NotPaidException


# from .producer_order import OrderProducer
# from .producer_payment import PaymentProducer
from .tasks import (
    task_order_process,
    notify_order_result,
    task_payment_process,
    notify_payment_result,
)
from ninja.security import HttpBasicAuth
from django.contrib.auth import authenticate, login


class BasicAuth(HttpBasicAuth):
    def authenticate(self, request, username, password):
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return {"message": "Login successful"}
        else:
            return {"message": "Login failed"}


# orderProducer = OrderProducer()
# paymentProducer = PaymentProducer()


api = NinjaAPI(title="Pos API")
menu = Router(tags=["menu"])


@functools.cache
@menu.get("/", response=List[MenuItemOut])
def list_menu(_):
    list = Menu.objects.all()
    return list


@functools.cache
@menu.get("/category/", response=List[MenuCategoryOut])
def list_category(_):
    list = MenuCategory.objects.all()
    return list


@menu.get("/{str:category}", response=List[MenuItemOut])
def list_menu_by_cat(_, category: str):
    menu_list = Menu.objects.filter(category__name__iexact=category)
    return menu_list


payment = Router(tags=["payment"])


def validate_payment_request(payload):
    """
    TBD
    """
    return True


@payment.post("/", response=PaymentOut, auth=BasicAuth())
def create_payment(_, payload: PaymentIn):
    payment_dict = vars(payload)

    if validate_payment_request(payload):
        return HttpResponse("Invalid input", status=422)

    task_payment.apply_async(
        args=(payment_dict["order_id"],),
        kwargs=payment_dict,
        link=notify_payment_result.s(),
    )
    return payment


order = Router(tags=["order"])


class OrderTicketResponse(Schema):
    ticket: str


def is_order_paid(order_id):
    payment_record = Payment.objects.filter(order_id=order_id)
    print(payment_record)
    return payment_record.exists()


@order.post("/", response=OrderTicketResponse, auth=BasicAuth())
def put_order(_, payload: List[OrderIn]):
    """
    Seperate orders even in same order_id/ticket, so that kitchen cook meals concurrently
    """
    # order_ids = [order.order_id for order in payload]
    # if not is_order_paid(order_ids[0]):
    #     raise NotPaidException

    redis_cache = caches["default"]
    redis_client = redis_cache.client.get_client()

    redis_client.incr(settings.ORDER_TICKET_COUNTER)
    ticket = int(redis_client.get(settings.ORDER_TICKET_COUNTER))
    total_quantity = 0

    for order_data in payload:
        order_dict = vars(order_data)

        """
        pydantic only validate data, add biz logic
        Meal name and price need match, or return error
        """
        menu = get_object_or_404(Menu, item_name=order_dict["item_name"])
        if menu.price * order_dict["quantity"] != order_dict["total_price"]:
            return HttpResponse("Invalid input", status=422)

        total_quantity += order_dict["quantity"]
        task_order_process.apply_async(
            args=(ticket,), kwargs=order_dict, link=notify_order_result.s()
        )

    redis_client.hset(
        f"{settings.KAFKA_ORDER_TOPIC}.{ticket}", "total_qty", total_quantity
    )
    redis_client.hset(f"{settings.KAFKA_ORDER_TOPIC}.{ticket}", "produced", 0)

    return {"ticket": ticket}


class OrderStatus(Schema):
    order_status: str


class BytesJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        return super().default(obj)


@order.get("/{int:ticket}", response=OrderStatus, auth=BasicAuth())
def get_order_status(_, ticket: int):
    redis_cache = caches["default"]
    redis_client = redis_cache.client.get_client()

    data = redis_client.hgetall(f"{settings.KAFKA_ORDER_TOPIC}.{ticket}")
    json_data = {key.decode(): value.decode() for key, value in data.items()}
    order_status = json.dumps(json_data, cls=BytesJSONEncoder)
    return {"order_status": order_status}


api.add_router("/", menu)
api.add_router("/order", order)
api.add_router("/payment", payment)
