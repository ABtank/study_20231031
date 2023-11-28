import random

from django.http import HttpResponse
from django.shortcuts import render

from .models import *


def generate_random_list(input_list):
    random_length = random.randint(0, len(input_list))
    random_items = random.sample(input_list, random_length)
    return random_items

def random_article():
    list_tags = Tag.objects.all()
    random_tag_ids = generate_random_list(list(list_tags.values_list('id', flat=True)))
    random_tags = Tag.objects.filter(id__in=random_tag_ids)
    category = ["E", "S", "IT", "F"]
    random_number = random.randint(0, len(category) - 1)
    len_text = random.randint(5, 100)
    numb = Article.objects.count() + 1
    authors = User.objects.all()
    num_acc = random.randint(0, len(authors) - 1)
    author = authors[num_acc]
    article = Article(author=author, title=f"title {numb}", anouncement=f"Анонс {numb}",
                      text=f"text {numb} " * len_text,
                      category=category[random_number])
    article.save()
    article.tags.set(random_tags)
    article.save()
    return article


def index(request):
    context = {}
    # article = Article.objects.all().first()
    # создание новости
    article = random_article()
    context['article'] = article
    return render(request, "news/index.html", context)


def news_list(request):
    context = {}
    # articles = Article.objects.all()
    articles = Article.objects.filter(author=request.user.id)
    context['articles'] = articles

    return render(request, "news/news.html", context)


def detail(request, id):
    context = {}
    # article = Article.objects.filter(id=id).first()
    article = Article.objects.get(id=id)
    context['article'] = article

    return HttpResponse(f'<h1>{article.title}</h1> <br> {article.text}')


def create_news(request):
    context = {}
    numb = len(Article.objects.all()) + 1
    author = User.objects.get(id=request.user.id)
    article = Article(author=author, title=f"title {numb}", anouncement=f"Анонс {numb}", text=f"text {numb} " * numb)
    article.save()
    context['article'] = article
    return HttpResponse(f'<h1>{article.title}</h1> <br> {article.text}')
