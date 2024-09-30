# your_project/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'to_do_backend.settings')

app = Celery('to_do_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Configure RabbitMQ as the broker
#app.conf.broker_url = 'amqp://user:pass@127.0.0.1:5672//'

app.autodiscover_tasks()
