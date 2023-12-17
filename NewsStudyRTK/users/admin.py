# регистрация моделей в панеле админа
from django.contrib import admin

from .models import *


class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender']
    list_filter = ['user', 'gender']


admin.site.register(Account, AccountAdmin)


@admin.register(FavoriteArticle)
class FavoriteArticleAdmin(admin.ModelAdmin):
    list_display = ['article', 'user', 'create_at']

@admin.register(MyFavoriteArticle)
class MyFavoriteArticleAdmin(admin.ModelAdmin):
    list_display = ['article', 'user', 'dt_create']
