# Generated by Django 4.2.7 on 2023-12-06 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'ordering': ['user'], 'verbose_name': 'Профиль', 'verbose_name_plural': 'Профили'},
        ),
    ]
