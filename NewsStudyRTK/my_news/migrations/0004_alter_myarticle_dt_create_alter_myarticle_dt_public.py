# Generated by Django 4.2.7 on 2023-12-06 13:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_news', '0003_alter_myarticle_dt_create_alter_myarticle_dt_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myarticle',
            name='dt_create',
            field=models.DateTimeField(auto_created=True, default=datetime.datetime(2023, 12, 6, 16, 49, 1, 985389), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='myarticle',
            name='dt_public',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 6, 16, 49, 1, 985389), verbose_name='Дата публикации'),
        ),
    ]