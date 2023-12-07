# регистрация моделей в панеле админа
from django.contrib import admin
from django.db.models import Count
from django.db.models.functions import Length

from .models import *


# class ArticleImageInline(admin.StackedInline):
class ArticleImageInline(admin.TabularInline):
    model = Image
    extra = 3
    readonly_fields = ('id', 'image_tag')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    ordering = ['-dt_public', 'title', 'author']
    list_display = ['id', 'title', 'symbols_count', 'author', 'dt_public', 'image_tag']
    list_filter = ['tags', 'author', 'category', 'dt_public']
    list_display_links = ['id']
    list_editable = ['title', 'author']
    # readonly_fields = ['author']
    # prepopulated_fields = {"slug": ('title',)}
    list_per_page = 10
    inlines = [ArticleImageInline, ]

    @admin.display(description="Длинна", ordering='_text_symbols')
    def symbols_count(self, article: Article):
        return f"Символов {len(article.text)}"

    # сортировка по symbols_count
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_text_symbols=Length('text'))
        return queryset


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'tag_count']
    list_filter = ['title', 'status']

    @admin.display(description="Новостей", ordering='tag_count')
    def tag_count(self, object):
        return f"Новостей {object.tag_count}"

    # сортировка по symbols_count
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(tag_count=Count('article'))
        return queryset


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_tag']
    list_filter = ['title']
