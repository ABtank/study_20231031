from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="my_news"),
    path('article/<int:article_id>/<slug:mode>', views.article, name="article"),  # статья
    path('create_my_article', views.create_my_article, name="create_my_article"),
    path('publication/<slug:target>', views.publication, name="publication"),
    path('profile', views.profile, name="profile"),
    path('info', views.info, name="info"),
    path('sign-in', views.signIn, name="signIn"),
]
