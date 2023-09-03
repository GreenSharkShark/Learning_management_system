from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название курса')
    preview = models.ImageField(upload_to='course_preview/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название курса')
    preview = models.ImageField(upload_to='lesson_preview/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='курс',
                               **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='плательщик', related_name='payments')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок',
                                    related_name='payments', **NULLABLE)
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс',
                                    related_name='payments', **NULLABLE)
    payment_date = models.DateTimeField(verbose_name='время и дата платежа')
    payment_amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    cash_payment = models.BooleanField(default=False, verbose_name='способ оплаты')

    def __str__(self):
        return f'{self.user} {self.paid_course if self.paid_course else self.paid_lesson}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
