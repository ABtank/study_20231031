from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="my_journal"),
    path('full_width', views.full_width, name="full_width"),
    path('gallery', views.gallery, name="gallery"),
    path('portfolio', views.portfolio, name="portfolio"),
    path('style_demo', views.style_demo, name="style_demo"),
]
