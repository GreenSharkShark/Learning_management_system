# Generated by Django 4.2.4 on 2023-09-14 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0017_rename_user_subscription_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.IntegerField(default=0, verbose_name='цена'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='price',
            field=models.IntegerField(default=0, verbose_name='цена'),
        ),
    ]
