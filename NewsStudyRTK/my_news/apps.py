from django.apps import AppConfig


class MyNewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_news'
    verbose_name = 'Мои новости (Д / З)'
