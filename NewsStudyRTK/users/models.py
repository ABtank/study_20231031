from django.db import models
from django.contrib.auth.models import User

from news.models import Article
from my_news.models import MyArticle


class Account(models.Model):
    gender_choices = (('M', 'Male'),
                      ('F', 'Female'),
                      ('N/A', 'Not answered'))

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    nickname = models.CharField(max_length=100)
    birthdate = models.DateField(null=True)
    gender = models.CharField(choices=gender_choices, max_length=20)
    # pip install Pillow для работы с файлами
    account_image = models.ImageField(default='default.jpg',
                                      upload_to='account_images')

    address = models.CharField(max_length=100, null=True)
    vk = models.CharField(max_length=100, null=True)
    instagram = models.CharField(max_length=100, null=True)
    telegram = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=20, null=True)
    first_name = models.CharField(max_length=40, null=True)
    last_name = models.CharField(max_length=40, null=True)
    is_all_agree = models.BooleanField(default=True)
    is_all_inform = models.BooleanField(default=True)

    class Meta:
        ordering = ['user']
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"{self.user.username}'s account"


class FavoriteArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    create_at = models.DateTimeField(auto_now_add=True)

class MyFavoriteArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    article = models.ForeignKey(MyArticle, on_delete=models.SET_NULL, null=True)
    dt_create = models.DateTimeField(auto_now_add=True)
