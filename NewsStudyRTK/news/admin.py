# регистрация моделей в панеле админа
from django.contrib import admin

from .models import *


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    ordering = ['-dt_public', 'title', 'author']
    list_display = ['id', 'title', 'author', 'dt_public']
    list_filter = ['tags', 'author', 'dt_public']
    list_display_links = ['id']
    list_editable = ['title', 'author']
    # readonly_fields = ['author']
    # prepopulated_fields = {"slug": ('title',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['title', 'status']
