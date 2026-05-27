import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service.settings')

app = Celery('service')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# -----------------------------
# PRODUCTION TASK SETTINGS
# -----------------------------

app.conf.task_track_started = True
app.conf.worker_prefetch_multiplier = 1
app.conf.task_acks_late = True