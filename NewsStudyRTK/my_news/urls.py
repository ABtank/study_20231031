from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name="my_news"),
    path('article/<int:article_id>/<slug:mode>', views.article, name="article"),  # статья
    path('create_my_article', views.create_my_article, name="create_my_article"),
    path('publication/<slug:target>', views.publication, name="publication"),
    path('profile', views.my_profile, name="my_profile"),
    path('info', views.info, name="info"),
    # path('sign-in', views.signIn, name="signIn"),
    path('my_registration', views.my_registration, name='my_registration'),
    path('sign_in', auth_views.LoginView.as_view(
        template_name='my_news/sign_in.html'), name='sign_in'),
    path('sign_out', auth_views.LogoutView.as_view(
        template_name='my_news/sign_out.html'), name='sign_out'),
    path('search_news/', views.search_news, name='search_news'),
    path('delete/<int:pk>', views.MyArticleDeleteView.as_view(), name="article_delete"),
    path('update/<int:pk>', views.MyArticleUpdateView.as_view(), name="article_update"),
]
