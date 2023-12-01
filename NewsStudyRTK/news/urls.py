from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="news_index"),
    path('news', views.news_list, name="news_list"),
    path('show/<int:id>', views.detail, name="news_detail"),
    path('create_article', views.create_article, name="create_article"),
]
