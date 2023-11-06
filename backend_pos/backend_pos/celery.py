from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend_pos.settings")

app = Celery("backend_pos")

# Load task modules from all registered Django app configs.
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_transport_options = {"topic_prefix": "celery"}
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()


@app.task
def my_periodic_task():
    print("Executing my_periodic_task")


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        60.0,  # Interval in seconds (60 seconds = 1 minute)
        my_periodic_task.s(),
    )
