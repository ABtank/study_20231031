# регистрация моделей в панеле админа
from django.contrib import admin

from .models import *


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'dt_public']
    list_filter = ['title', 'author', 'dt_public']




class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['title', 'status']


admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
