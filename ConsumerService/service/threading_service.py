import json
import sys
import threading
from django.conf import settings
from confluent_kafka import Consumer
from confluent_kafka import KafkaError
from confluent_kafka import KafkaException

# We want to run thread in an infinite loop
running = True

# Topic

import signal
import sys


def signal_handler(sig, frame):
    print("Stopping")
    instance = UserCreatedServant()
    instance.shut_down()


signal.signal(signal.SIGINT, signal_handler)


class UserCreatedServant(threading.Thread):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating the consumer thread")
            print("Ctl+c to gracefully stop the service")
            cls._instance = super(UserCreatedServant, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

    def __init__(self):
        threading.Thread.__init__(self)
        # Create consumer
        self.consumer = Consumer(settings.KAFKA_CONFIG)
        self.event = threading.Event()

    def shut_down(self):
        self.event.set()

    def run(self):
        print("Inside Service :  Created Listener ")
        try:
            # Subcribe to topic
            self.consumer.subscribe([settings.KAFKA_TOPIC])
            while running:
                # Poll for message
                msg = self.consumer.poll(timeout=1)
                if self.event.is_set():
                    print("Stopped")

                    break

                if msg is None:
                    continue
                # Handle Error
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        sys.stderr.write(
                            "%% %s [%d] reached end at offset %d\n"
                            % (msg.topic(), msg.partition(), msg.offset())
                        )
                elif msg.error():
                    raise KafkaException(msg.error())
                else:
                    # Handle Message
                    print("---------> Got message Do Something....")
                    message = json.loads(msg.value().decode("utf-8"))
                    print(message)
        finally:
            # Close down consumer to commit final offsets.
            self.consumer.close()
