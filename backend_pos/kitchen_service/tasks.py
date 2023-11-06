from time import sleep
from celery import shared_task
import random
import json
from celery import shared_task
from .notifications import send_notification
from django.utils.timezone import now
from django.conf import settings
from django.core.cache import caches


class TaskFailureException(Exception):
    def __init__(self, message):
        super().__init__(message)


def do_cook_moc():
    moc_value = random.randint(1, 5)
    sleep(moc_value * 10)


@shared_task
def on_cook_meal_task_success(result, context):
    print(f"Task succeeded with result: {result} {context}")


@shared_task
def on_cook_meal_task_failure(result, context):
    print(f"Task failed with error: {result} {context}")


@shared_task(soft_time_limit=360, time_limit=720)
def task_cook_meal(ticket, meal_name):
    # do_cook_moc()
    redis_cache = caches["default"]
    redis_client = redis_cache.client.get_client()
    key = f"{settings.KAFKA_ORDER_TOPIC}.{ticket}"

    with redis_client.pipeline() as pipe:
        pipe.hget(key, meal_name)
        pipe.hget(key, "produced")
        pipe.hget(key, "total_qty")
        """ Get Keys in single redis access"""
        (
            meal_qty,  # {left:done}
            produced,
            total_qty,
        ) = pipe.execute()
        left, done = meal_qty.decode("utf-8").split(":")
        left = int(left) - 1
        done = int(done) + 1

        pipe.hset(key, meal_name, f"{left}:{done}")
        pipe.hset(key, "produced", int(produced) + 1)
        if int(total_qty) == int(produced) + 1:
            """
            Cache finisked ticket in redis for 20 minutes
            """
            pipe.setex(f"ticket.ready.{ticket}", 20 * 60, ticket)
            """
            Cache finished ticket detail in 15 seconds
            """
            pipe.expire(key, 15)
            """SSE Notification"""
            send_notification(
                event="toasts",
                subject="Cook Done",
                message=f"{ticket} is done.",
                ts=now(),
                template="board/toast.html",
            )

        pipe.execute()

        return True
