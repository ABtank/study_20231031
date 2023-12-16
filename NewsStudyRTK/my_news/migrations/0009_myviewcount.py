# Generated by Django 4.2.7 on 2023-12-15 23:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_news', '0008_alter_myarticle_dt_create_alter_myarticle_dt_public'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyViewCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('dt_view', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='my_news.myarticle')),
            ],
            options={
                'ordering': ('-dt_view',),
                'indexes': [models.Index(fields=['-dt_view'], name='my_news_myv_dt_view_9a1493_idx')],
            },
        ),
    ]
