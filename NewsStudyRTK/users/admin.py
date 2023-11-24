# регистрация моделей в панеле админа
from django.contrib import admin

from .models import *


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender']
    list_filter = ['user', 'gender']


admin.site.register(Account, ArticleAdmin)
