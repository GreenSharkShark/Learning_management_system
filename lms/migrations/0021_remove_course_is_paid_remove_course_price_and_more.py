# Generated by Django 4.2.4 on 2023-09-19 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0020_course_is_paid_lesson_is_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='is_paid',
        ),
        migrations.RemoveField(
            model_name='course',
            name='price',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='is_paid',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='price',
        ),
        migrations.RemoveField(
            model_name='payments',
            name='session',
        ),
        migrations.AddField(
            model_name='course',
            name='last_update_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]