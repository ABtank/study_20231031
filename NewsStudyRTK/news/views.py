import json
import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection, reset_queries
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView, UpdateView
from django.db.models import Count, Q

from .forms import ArticleForm, ImagesFormSet
from .models import *


# URL:    path('search_auto/', views.search_auto, name='search_auto'),
def search_auto(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        q = request.GET.get('term', '')
        articles = Article.objects.filter(title__icontains=q)
        results = []
        for a in articles:
            results.append(a.title)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/news_detail.html'
    context_object_name = 'article'


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'news/create_article.html'
    fields = ['title', 'anouncement', 'text', 'tags']

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdateView, self).get_context_data(**kwargs)
        current_object = self.object
        images = Image.objects.filter(article=current_object)
        context['image_form'] = ImagesFormSet(instance=current_object)
        return context

    def post(self, request, **kwargs):
        request.POST = request.POST
        current_object = Article.objects.get(id=request.POST['image_set-0-article'])
        deleted_ids = []
        for i in range(int(request.POST['image_set-TOTAL_FORMS'])):  # удаление всех по галочкам
            field_delete = f'image_set-{i}-DELETE'
            field_image_id = f'image_set-{i}-id'
            if field_delete in request.POST and request.POST[field_delete] == 'on':
                image = Image.objects.get(id=request.POST[field_image_id])
                image.delete()
                deleted_ids.append(field_image_id)

                # тут же удалить картинку из request.FILES
        # Замена картинки
        for i in range(int(request.POST['image_set-TOTAL_FORMS'])):  # удаление всех по галочкам
            field_replace = f'image_set-{i}-image'  # должен быть в request.FILES
            field_image_id = f'image_set-{i}-id'  # этот файл мы заменим
            if field_replace in request.FILES and request.POST[
                field_image_id] != '' and field_image_id not in deleted_ids:
                image = Image.objects.get(id=request.POST[field_image_id])  #
                image.delete()  # удаляем старый файл
                for img in request.FILES.getlist(field_replace):  # новый добавили
                    Image.objects.create(article=current_object, image=img, title=img.name)
                del request.FILES[field_replace]  # удаляем использованный файл
        if request.FILES:  # Добавление нового изображения
            print('!!!!!!!!!!!!!!!!!', request.FILES)
            for input_name in request.FILES:
                for img in request.FILES.getlist(input_name):
                    print('###############', img)
                    Image.objects.create(article=current_object, image=img, title=img.name)

        return super(ArticleUpdateView, self).post(request, **kwargs)


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('news_list')
    template_name = 'news/delete_article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_object = self.object
        images = Image.objects.filter(article=current_object)
        context['images'] = images
        return context


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
    search_input = ''
    if request.method == "POST":
        filters = Q()  # Создаем пустой объект Q
        print(request.POST)
        selected = int(request.POST.get('author_filter'))
        if selected > 0:
            filters &= Q(author=selected)

        search_input = request.POST.get('search_input')
        if len(search_input) > 0:
            filters &= Q(title__icontains=search_input)
        else:
            search_input = ''

        articles = Article.objects.select_related("author").prefetch_related('tags').annotate(
            Count('tags')).order_by('-dt_public', 'title').filter(filters)
    else:
        articles = (Article.objects
                    .select_related("author")  # select_related - один ко многим
                    .prefetch_related('tags')  # prefetch_related - многие ко многим
                    .annotate(Count('tags'))  # аннотирование - добавляет колонку к запросу
                    .order_by('-dt_public', 'title')  # сортировка начиная с самых новых
                    .all())
    print(connection.queries)
    context['articles'] = articles
    context['author_list'] = author_list
    context['selected'] = selected
    context['search_input'] = search_input

    return render(request, "news/news.html", context)


# человек не аутентифицирован - отправляем на страницу другую
# @login_required(login_url="news_list")
@login_required(login_url=settings.LOGOUT_REDIRECT_URL)
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            if current_user.id is not None:  # проверили что не аноним
                new_article = form.save(commit=False)  # сохранение без коммита
                new_article.author = current_user
                new_article.save()  # сохраняем в БД
                form.save_m2m()
                for img in request.FILES.getlist('image_field'):
                    Image.objects.create(article=new_article, image=img, title=img.name)
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
