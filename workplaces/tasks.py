from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def process_workplace_creation(workplace_id):
    # Пример задачи: логирование создания workplace
    logger.info(f"Processing creation of workplace with ID: {workplace_id}")
    # Здесь можно добавить логику, например, отправка email, обновление кэша и т.д.
