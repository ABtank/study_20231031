import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


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


# свой фильтр
class PublishedToday(models.Manager):
    def get_queryset(self):
        return super(PublishedToday, self).get_queryset().filter(dt_public__gte=datetime.date.today())


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

    # уникальное поле для ссылок вместо id
    # slug = models.SlugField()

    # общие методы
    objects = models.Manager()
    # свой фильтр
    publishedToday = PublishedToday()

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


class Image(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='article_image/')

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image is not None:
            return mark_safe(f"<img src='{self.image.url}' title='{self.title}' style=\"width: auto;height: 150px;\">")
        else:
            return '(not image)'
