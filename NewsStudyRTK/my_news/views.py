import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.shortcuts import render, redirect

from .forms import MyArticleForm
from .models import MyTag, MyArticle, User


def generate_random_list(input_list):
    random_length = random.randint(0, len(input_list))
    random_items = random.sample(input_list, random_length)
    return random_items


def random_article(target):
    list_tags = MyTag.objects.all().values_list('id', flat=True)
    random_tag_ids = generate_random_list(list(list_tags))
    random_tags = MyTag.objects.filter(id__in=random_tag_ids)
    category = ['hot', 'fresh', 'subscription']
    random_number = random.randint(0, len(category) - 1)
    len_text = random.randint(50, 100)
    numb = MyArticle.objects.count() + 1
    authors = User.objects.all()
    num_acc = random.randint(0, len(authors) - 1)
    author = authors[num_acc]
    article = MyArticle(author=author, title=f"title-{target} {numb}",
                        anouncement=f"Анонс-{target} {numb}" * (len_text // 5),
                        text=f"{target} {numb} " * len_text,
                        category=target)
    article.save()
    article.tags.set(random_tags)
    article.save()
    return article


def get_category():
    category = ['hot', 'fresh', 'subscription']
    random_number = random.randint(0, len(category) - 1)
    return category[random_number]


# Create your views here.
def index(request):
    context = {}
    return render(request, "my_news/index.html", context)


def publication(request, target):
    random_article(target)
    context = {"target": target}
    tags_list = (MyTag.objects
                 .annotate(num_articles=Count('myarticle'))
                 .all())
    authors_list = User.objects.annotate(Count('myarticle', distinct=True))
    context['tags_list'] = tags_list
    context['authors_list'] = authors_list

    # Фильтр
    tags_selected = []
    authors_selected = []
    filters = Q()  # Создаем пустой объект Q
    filters &= Q(category__iexact=target)
    if request.method == "POST":
        tags_selected = [int(tag_id) for tag_id in request.POST.getlist('tags_filter') if len(tag_id) > 0]
        if len(tags_selected) > 0:
            filters &= Q(tags__in=tags_selected)

        authors_selected = [int(tag_id) for tag_id in request.POST.getlist('authors_filter') if len(tag_id) > 0]
        if len(authors_selected) > 0:
            filters &= Q(author__in=authors_selected)

    match target:
        case 'hot' | 'fresh' | 'subscription':
            articles = (MyArticle.objects
                        .select_related("author")
                        .prefetch_related('tags')
                        .annotate(Count('tags'))
                        .filter(filters)
                        .order_by('-dt_public', 'title')
                        .all())
        case _:
            return render(request, "my_news/custom_404.html", {'exception': "страница не найдена"})

    context['articles'] = articles
    context['tags_list'] = tags_list
    context['tags_selected'] = tags_selected
    context['authors_selected'] = authors_selected
    return render(request, "my_news/publication.html", context)


def article(request, article_id, mode):
    context = {}

    article = (MyArticle.objects
               .select_related("author")
               .prefetch_related('tags')
               .annotate(Count('tags'))
               .filter(id=article_id)
               .first())
    if article is None:
        messages.error(request, "Статья не найдена!")
        return redirect('publication', target='fresh')

    context["article"] = article
    match mode:
        case 'view':
            print('view')
        case 'edit':
            if request.method == "POST":
                print("POST")
                form = MyArticleForm(request.POST, instance=context["article"])
                print(form.changed_data)
                current_user = request.user
                if current_user.id is not None:  # проверили что не аноним
                    new_article = form.save()
                    messages.success(request, f'Обновлена статья  №{article_id} - "{new_article.title}"!')
                    context["article"] = (MyArticle.objects
                                          .select_related("author")
                                          .prefetch_related('tags')
                                          .annotate(Count('tags'))
                                          .get(id=new_article.id))
                    return redirect('article', article_id=article_id, mode='view')
                else:
                    messages.error(request, "Не авторизованы")
            else:
                print('edit GET')
                context["form"] = MyArticleForm(instance=context["article"])
        case _:
            return render(request, "my_news/custom_404.html", {'exception': "страница не найдена"})
    print(context)
    return render(request, "my_news/article.html", context)


@login_required(login_url="my_news")
def create_my_article(request):
    if request.method == 'POST':
        form = MyArticleForm(request.POST)
        if form.is_valid():
            current_user = request.user
            if current_user.id is not None:  # проверили что не аноним
                new_article = form.save(commit=False)  # сохранение без коммита
                new_article.category = get_category()  # рандомно устанавливаем категорию
                new_article.save()  # сохраняем в БД
                form.save_m2m()
                messages.success(request, f"Создана новая статья №{new_article.id} - {new_article.title}")
                messages.success(request, f"Поздравляем! Ваша статья попала в раздел {new_article.category}!")
                if request.POST.get('saveAndNew') is not None:
                    form = MyArticleForm()
                else:
                    return redirect(f'article/{new_article.id}/view')
            else:
                messages.error(request, "Не авторизованы")
    else:
        form = MyArticleForm()
    return render(request, 'my_news/create_article.html', {'form': form})


def profile(request):
    context = {}
    if request.method == "POST":
        messages.success(request, f'Обновили типа данные! {request.POST.get("username")}')
    else:
        print("GET")
    return render(request, "my_news/profile.html", context)


def info(request):
    context = {}
    return render(request, "my_news/info.html", context)


def signIn(request):
    context = {}
    return render(request, "my_news/sign-in.html", context)


def custom_404(request, exception):
    context = {'exception': exception}
    return render(request, "my_news/custom_404.html", context)
