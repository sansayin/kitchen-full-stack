from time import sleep
from celery import shared_task
import json
from .producer_order import OrderProducer
from .producer_payment import PaymentProducer
from order_service.models import Order, Payment
import random
from celery import shared_task


class TaskFailureException(Exception):
    def __init__(self, message):
        super().__init__(message)


@shared_task()
def periodic_task():
    """
    TBD
    Clean Up Redis Cache
    Config it in Django Admin Page
    """
    print("My periodic task executed")


@shared_task()
def notify_payment_result(result):
    """
    TBD
    Notify front end payment status; True|False
    """
    print(f"notify_payment_result-{result}")


@shared_task()
def task_payment_process(ticket, **payment_detail):
    """
    TBD

    Moc payment process
    Due to GDPR, no Credit Card or Personal Info will store
    """
    moc_value = random.randint(0, 9) < 2
    sleep(10)
    if moc_value:
        payment = Payment(**payment_detail)
        payment.save()
        paymentProducer = PaymentProducer()
        paymentProducer.publish(ticket=ticket, **payment_detail)
        return True
    raise TaskFailureException("Task failed due to some reason")


@shared_task()
def notify_order_result(anything):
    """
    TBD
    """
    print(f"notify_order_result- {anything}")


@shared_task(soft_time_limit=30, time_limit=70)
def task_order_process(ticket, **meal_detail):
    """
    Persist order in DB and send to kafka MQ
    """
    order = Order(**meal_detail, done=False)
    order.save()
    del meal_detail["total_price"]
    meal_detail["value"] = json.dumps(meal_detail)
    orderProducer = OrderProducer()
    orderProducer.publish(ticket=ticket, **meal_detail)
    return True


@shared_task(soft_time_limit=36, time_limit=72)
def task_send_mail(ticket, **kwargs):
    """
    TBD
    Send mail task, use it to send receite or for customer care
    """
    moc_value = random.randint(5, 20)
    sleep(moc_value)
    return True
