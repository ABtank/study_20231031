# Generated by Django 4.2.7 on 2023-11-23 00:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_create', models.DateTimeField(auto_created=True, verbose_name='Дата создания')),
                ('title', models.CharField(default='', max_length=50, verbose_name='Название')),
                ('anouncement', models.TextField(max_length=256, verbose_name='Аннотация')),
                ('text', models.TextField(verbose_name='Текст новости')),
                ('dt_public', models.DateTimeField(auto_now=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]