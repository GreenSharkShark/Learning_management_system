# Generated by Django 4.2.4 on 2023-09-10 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0006_course_owner_lesson_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='vido_url',
            field=models.URLField(blank=True, null=True, verbose_name='ссылка на видео'),
        ),
    ]
