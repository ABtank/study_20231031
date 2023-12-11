# регистрация моделей в панеле админа
from django.contrib import admin

from .models import *


class MyArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'dt_public']
    list_filter = ['tags', 'category', 'author', 'dt_public']


class MyTagAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['title', 'status']


admin.site.register(MyTag, MyTagAdmin)
admin.site.register(MyArticle, MyArticleAdmin)
