from django.contrib import messages
from django.shortcuts import render

from .models import Article


# Create your views here.
def index(request):
    context = {}
    return render(request, "my_news/index.html", context)


def publication(request, target):
    context = {"target": target}
    article1 = Article(1, "hot Новость 1", "Текст 1", "03.11.23", 1, "дом", 0)
    article2 = Article(2, "fresh Новость 2", "Текст 2", "04.11.23", 0, "работа", 0)
    article3 = Article(3, "subscription Новость 3", "Текст 3", "05.11.23", 0, "огород", 1)
    match target:
        case 'hot':
            context["article"] = article1
        case 'fresh':
            context["article"] = article2
        case 'subscription':
            context["article"] = article3
        case _:
            return render(request, "my_news/custom_404.html", {'exception': "страница не найдена"})
    return render(request, "my_news/publication.html", context)


def article(request, article_id, mode):
    alert = ""
    if request.method == "POST":
        print("POST")
        title = request.POST.get('title')
        text = request.POST.get('text')
        date = request.POST.get('date')
        if article_id > 0:
            print('Создана статья!')
            messages.success(request, f'Обновлена статья "{title}"! №{article_id}')
        else:
            messages.success(request, f'Создана статья! "{title}"')
    else:
        print("GET")

    context = {}
    # БД
    article1 = Article(1, "Новость 1", "Текст 1", "03.11.23", 1, "дом", 0)
    article2 = Article(2, "Новость 2", "Текст 2", "04.11.23", 0, "работа", 0)
    article3 = Article(3, "Новость 3", "Текст 3", "05.11.23", 0, "огород", 1)
    article0 = Article(0, "", "", "", 0, "", 0)
    arr_news = [article1, article2, article3]
    if article_id not in list(map(lambda x: int(x.article_id), arr_news)):
        context["article"] = article0
    else:
        context["article"] = list(filter(lambda el: el.article_id == article_id, arr_news))[0]

    match mode:
        case 'view':
            print('view')
        case 'edit':
            print('edit')
        case _:
            return render(request, "my_news/custom_404.html", {'exception': "страница не найдена"})
    print(list(map(lambda x: int(x.article_id), arr_news)))
    print(context["article"])
    return render(request, "my_news/article.html", context)


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
