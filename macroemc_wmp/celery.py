from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from .utils import log

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "macroemc_wmp.settings")

app = Celery("macroemc_wmp")

app.config_from_object("django.conf:settings", namespace="CELERY")
log.info(
    "broker: %s, backend: %s, broker_connection_retry_on_startup: %s",
    settings.CELERY_BROKER_URL,
    settings.CELERY_RESULT_BACKEND,
    settings.CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP,
)

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
