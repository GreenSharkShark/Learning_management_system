from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """
    Класс для создания суперпользователя. Данные заполните сами
    """
    def handle(self, *args, **options):
        user = User.objects.create(
            email='email2',
            first_name='first_name',
            last_name='last_name',
            is_staff=False,
            is_superuser=False,
            is_active=True
        )
        user.set_password('set_password')
        user.save()
