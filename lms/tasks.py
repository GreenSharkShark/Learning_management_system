from datetime import datetime, timedelta
from django.core.cache import cache
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from celery import shared_task
from lms.models import Course, Subscription
from users.models import User


@shared_task
def check_course_updates() -> None:
    """
    Функция проверяет дату последнего обновления объекта и сравнивает с кэшем,
    если объект обновился - отправляет сообщение
    :return: None
    """
    last_check_time = cache.get('last_check_time')
    if not last_check_time:
        cache.set('last_check_time', datetime.now(), 100)
        last_check_time = cache.get('last_check_time')

    updated_courses = Course.objects.filter(last_update_date__gt=last_check_time)
    if not updated_courses:
        return

    subscriptions = Subscription.objects.filter(course__in=updated_courses).select_related('owner').distinct()
    emails_to_send = list(subscriptions.values_list('owner__email', flat=True))
    send_mail(
        subject='Обновление курса',
        message='Курс обновился',
        from_email=EMAIL_HOST_USER,
        recipient_list=emails_to_send
    )
    cache.set('last_check_time', datetime.now(), 100)


@shared_task
def check_last_login() -> None:
    """
    Функция проверяет пользователей которые не авторизовывались больше 30 дней
    и блокирует устанавливая флаг is_active = False
    :return: None
    """
    current_datetime = datetime.now()
    thirty_days_ago = current_datetime - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=thirty_days_ago)
    inactive_users.update(is_active=False)
