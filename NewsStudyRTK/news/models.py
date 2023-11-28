import datetime

from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    title = models.CharField(max_length=80)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"title = {self.title} status = {self.status}"

    # метаданные модели
    class Meta:
        ordering = ['title', 'status']
        verbose_name = "Тег"
        verbose_name_plural = "Теги"




class Article(models.Model):
    categories = (("E", "Economics"),
                  ("S", "Science"),
                  ("IT", "IT"),
                  ("F", "Fails"),
                  )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Автор")
    title = models.CharField(verbose_name="Название", max_length=50, default='')
    anouncement = models.TextField(verbose_name="Аннотация", max_length=256, help_text="это аннотация")
    text = models.TextField("Текст новости")
    dt_public = models.DateTimeField(verbose_name="Дата публикации", auto_now=True)
    dt_create = models.DateTimeField(verbose_name="Дата создания", auto_created=True, default=datetime.datetime.now())
    category = models.CharField(choices=categories, max_length=20, verbose_name="Категории")

    tags = models.ManyToManyField(to=Tag, blank=True, verbose_name="Теги")

    # методы модели
    def __str__(self):
        return f"{self.title} от: {self.dt_public.date()}"

    def get_absolute_url(self):
        return f"/news/show/{self.pk}"

    # метаданные модели
    class Meta:
        ordering = ['-dt_public', 'title']
        verbose_name = "Новость"
        verbose_name_plural = "Новости"