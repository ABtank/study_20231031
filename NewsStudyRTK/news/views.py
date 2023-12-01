import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection, reset_queries
from django.db.models import Count

from .forms import ArticleForm
from .models import *


def generate_random_list(input_list):
    random_length = random.randint(0, len(input_list))
    random_items = random.sample(input_list, random_length)
    return random_items


def random_article():
    list_tags = Tag.objects.all().values_list('id', flat=True)
    random_tag_ids = generate_random_list(list(list_tags))
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
    # articles_today = Article.publishedToday.all()
    # print(articles_today)
    # print(datetime.date.today())
    # создание новости
    article = random_article()
    article = (Article.objects
               .select_related("author")
               .prefetch_related('tags')
               .annotate(Count('tags'))
               .get(id=article.id))
    context['article'] = article
    return render(request, "news/index.html", context)


def news_list(request):
    context = {}

    author_list = User.objects.annotate(Count('article', distinct=True))
    # for usr in author_list:
    #     print(usr.id, usr.article__count)
    selected = 0
    if request.method == "POST":
        print(request.POST)
        selected = int(request.POST.get('author_filter'))
        if selected == 0:
            articles = Article.objects.select_related("author").prefetch_related('tags').annotate(
                Count('tags')).order_by('-dt_public', 'title').all()
        else:
            articles = Article.objects.select_related("author").prefetch_related('tags').annotate(
                Count('tags')).order_by('-dt_public', 'title').filter(author=selected)
    else:
        articles = (Article.objects
                    .select_related("author")  # select_related - один ко многим
                    .prefetch_related('tags')  # prefetch_related - многие ко многим
                    .annotate(Count('tags'))  # аннотирование - добавляет колонку к запросу
                    .order_by('-dt_public', 'title')  # сортировка начиная с самых новых
                    .all())
        print(articles)
    print(connection.queries)
    context['articles'] = articles
    context['author_list'] = author_list
    context['selected'] = selected

    return render(request, "news/news.html", context)


def detail(request, id):
    context = {}
    # article = Article.objects.filter(id=id).first()
    article = Article.objects.get(id=id)
    context['article'] = article

    return HttpResponse(f'<h1>{article.title}</h1> <br> {article.text}')


# человек не аутентифицирован - отправляем на страницу другую
@login_required(login_url="news_list")
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            current_user = request.user
            if current_user.id is not None:  # проверили что не аноним
                new_article = form.save(commit=False)  # сохранение без коммита
                new_article.author = current_user
                new_article.save()  # сохраняем в БД
                form.save_m2m()
                messages.success(request, f"Создана новая запись {new_article.title}")
                if request.POST.get('saveAndNew') is not None:
                    form = ArticleForm()
                else:
                    return redirect('news_list')
            else:
                messages.error(request, "Не авторизованы")
    else:
        form = ArticleForm()
    return render(request, 'news/create_article.html', {'form': form})
