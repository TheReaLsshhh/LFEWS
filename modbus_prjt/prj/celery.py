from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prj.settings')

app = Celery('prj')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# Namespace 'CELERY' means all celery-related configs in settings should start with 'CELERY_'.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks in your installed apps.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

if os.name == 'nt':  # Windows
    import multiprocessing
    multiprocessing.set_start_method('spawn', force=True)
