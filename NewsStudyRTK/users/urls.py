from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name="users_index"),
    path('contact_page/', views.contact_page, name="contact_page"),
    path('registration/', views.registration, name="registration"),
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='users/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/update', views.profile_update, name='profile_update'),
    path('password', views.password_update, name='password'),
    path('favorites/<int:article_id>', views.add_to_favorites, name='favorites'),
    path('my_favorites/<int:article_id>', views.add_to_my_favorites, name='my_favorites'),
    path('api/my_favorites', views.api_my_favorites, name='api_my_favorites'),
]
