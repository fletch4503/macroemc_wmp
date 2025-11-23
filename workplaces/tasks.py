from celery import shared_task
from .models import Workplaces, Staff
from macroemc_wmp.utils import log
import time


@shared_task(name="Create_wp_task")
def create_wp_task(workplace_id: int = None):
    wp = Workplaces.objects.get(id=workplace_id)
    # Получаем список сотрудников данного отдела для рассылки
    staff_emails = Staff.objects.filter(department=wp.department)
    if staff_emails:
        log.info("Получили в задачу создания рабочего места: %s список для рассылки: %s", workplace_id, staff_emails)
        for stemail in staff_emails:
            # Эмулируем отправку
            log.warning("Отправили письмо с оповещением на email: %s", stemail)
            time.sleep(3)

    return {
        "status": "SUCCESS",
        "state": "Уведомления отправлены",
    }