from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="news_index"),
    path('news', views.news_list, name="news_list"),
    # pk надо указывать а не поле
    path('show/<int:pk>', views.ArticleDetailView.as_view(), name="news_detail"),
    path('update/<int:pk>', views.ArticleUpdateView.as_view(), name="news_update"),
    path('delete/<int:pk>', views.ArticleDeleteView.as_view(), name="news_delete"),
    path('create_article', views.create_article, name="create_article"),
]
