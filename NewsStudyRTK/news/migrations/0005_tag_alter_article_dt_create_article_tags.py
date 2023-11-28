# Generated by Django 4.2.7 on 2023-11-24 00:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_article_category_alter_article_dt_create'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ['title', 'status'],
            },
        ),
        migrations.AlterField(
            model_name='article',
            name='dt_create',
            field=models.DateTimeField(auto_created=True, default=datetime.datetime(2023, 11, 24, 3, 54, 34, 646051), verbose_name='Дата создания'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, to='news.tag', verbose_name='Теги'),
        ),
    ]