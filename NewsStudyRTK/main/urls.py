from django.contrib import admin
from django.urls import path

from . import views
from my_news.views import index

urlpatterns = [
    path('', index, name="home"),
    path('about', views.about, name="about"),
    path('contacts', views.contacts, name="contacts"),
    path('sidebar', views.sidebar, name="sidebar"),
    path('calc/<int:a>/<slug:operation>/<int:b>',views.get_demo),
]
