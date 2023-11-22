from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="news_index"),
    # path('news', views.about, name="news_list"),
]
