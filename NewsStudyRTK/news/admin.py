# регистрация моделей в панеле админа
from django.contrib import admin
from django.db.models import Count
from django.db.models.functions import Length

from .models import *


class ArticleFilter(admin.SimpleListFilter):
    title = 'Наш фильтр'
    parameter_name = 'text'  # имя в урле

    def lookups(self, request, model_admin):
        return [
            ('S', "Короткие, <100 зн."),
            ('M', "Средние, 100 - 500 зн."),
            ('L', "Длинные, >500 зн."),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'S':
            return queryset.annotate(teext_len=Length('text')).filter(teext_len__lt=100)
        elif self.value() == 'M':
            return queryset.annotate(teext_len=Length('text')).filter(teext_len__lt=500, teext_len__gte=100)
        elif self.value() == 'L':
            return queryset.annotate(teext_len=Length('text')).filter(teext_len__gte=500)


# class ArticleImageInline(admin.StackedInline):
class ArticleImageInline(admin.TabularInline):
    model = Image
    extra = 3
    readonly_fields = ('id', 'image_tag')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    ordering = ['-dt_public', 'title', 'author']
    list_display = ['id', 'title', 'symbols_count', 'author', 'dt_public', 'image_tag']
    list_filter = ['tags', 'author', 'category', 'dt_public',ArticleFilter]
    list_display_links = ['id']
    list_editable = ['title', 'author']
    # readonly_fields = ['author']
    # prepopulated_fields = {"slug": ('title',)}
    list_per_page = 10
    inlines = [ArticleImageInline, ]
    # __icontains функция поиска без учета регистра
    search_fields = ['title__icontains', 'tags__title__icontains']
    filter_horizontal = ['tags']

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
    actions = ['set_false', 'set_true']

    @admin.display(description="Новостей", ordering='tag_count')
    def tag_count(self, object):
        return f"Новостей {object.tag_count}"

    # действия
    @admin.action(description="Активировать выбранные теги")
    def set_true(self, request, queryset):
        amount = queryset.update(status=True)
        self.message_user(request, f"Активировано {amount} тегов")

    # действие
    @admin.action(description="ДЕактивировать выбранные теги")
    def set_false(self, request, queryset):
        amount = queryset.update(status=False)
        self.message_user(request, f"ДЕактивировано {amount} тегов")

    # сортировка по symbols_count
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(tag_count=Count('article'))
        return queryset


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_tag']
    list_filter = ['title']
