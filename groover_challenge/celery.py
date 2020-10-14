# -*- coding: utf-8 -*-
import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'groover_challenge.settings')

app = Celery('groover_challenge')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
