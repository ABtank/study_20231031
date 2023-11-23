# регистрация моделей в панеле админа
from django.contrib import admin

from .models import *


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'dt_public']
    list_filter = ['title', 'author', 'dt_public']


admin.site.register(Article, ArticleAdmin)
