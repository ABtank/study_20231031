# регистрация моделей в панеле админа
from django.contrib import admin

from .models import *

class MyArticleImageInline(admin.TabularInline):
    model = MyImage
    extra = 3
    readonly_fields = ('id', 'image_tag')

@admin.register(MyArticle)
class MyArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'image_tag', 'dt_public']
    list_filter = ['tags', 'category', 'author', 'dt_public']
    inlines = [MyArticleImageInline, ]


@admin.register(MyTag)
class MyTagAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['title', 'status']

@admin.register(MyImage)
class MyImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_tag']
    list_filter = ['title']