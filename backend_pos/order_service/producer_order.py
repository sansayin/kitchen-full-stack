import uuid
import json
from confluent_kafka import Producer

from django.conf import settings
from django.core.cache import caches


producer_config = {
    "bootstrap.servers": ",".join(settings.KAFKA_BROKERS),
    "acks": "all",
    "enable.idempotence": "true",
}


class OrderProducer:
    def __init__(self, prefix=None) -> None:
        self.producer = Producer(producer_config)
        self.prefix = prefix

    def publish(self, ticket, order_id, meal_id, item_name, quantity, value):
        redis_cache = caches["default"]
        redis_client = redis_cache.client.get_client()

        """
        1.Set meta data in msg headers
        2.Callback when msg successfully enqueue
        """

        class Event:
            def __init__(self, ticket, order_id, meal_id, item_name, quantity):
                self.headers = {
                    "ticket": str(ticket),
                    "order_id": str(order_id),
                    "meal_id": str(meal_id),
                    "item_name": str(item_name),
                    "quantity": str(quantity),
                }

            def callback(self, err, msg):
                if err is not None:
                    print("Process Erroe")
                else:
                    hset_key = f"{settings.KAFKA_ORDER_TOPIC}.{self.headers['ticket']}"
                    item_qty = f"{self.headers['quantity']}: 0"  # meal total:done
                    print(item_qty)
                    redis_client.hset(
                        hset_key,
                        self.headers["item_name"],
                        item_qty,
                    )

                #  redis_client.expire(hset_key, 60 * 60)

        self.producer.poll(0)
        e = Event(ticket, order_id, meal_id, item_name, quantity)
        self.producer.produce(
            settings.KAFKA_ORDER_TOPIC,
            key=uuid.uuid4().bytes,
            value=value.encode("utf-8"),
            headers=e.headers,
            callback=e.callback,
        )
        self.producer.flush()
        return
