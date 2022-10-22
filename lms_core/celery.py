

import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_core.settings')
app = Celery('lms_core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()