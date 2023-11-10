from django.shortcuts import render
from django.http import HttpResponse
from .models import News


def index(request):
    value = 0
    arr_numbers = ["раз", "два", "три"]
    new1 = News("Новость 1", "Текст 1", "07.11.23")
    new2 = News("Новость 2", "Текст 2", "08.11.23")
    new3 = News("Новость 3", "Текст 3", "09.11.23")
    arr_news = [new1, new2, new3]

    dictionary = {1:"один", 2: "два"}

    context = {"title": "Страница главная",
               "Header1": "Заголовок страницы",
               "value": value,
               "numbers": arr_numbers,
               "news": arr_news,
               "dictionary": dictionary,
               }

    return render(request, "main/index.html", context)


def about(request):
    return render(request, "main/about.html")


def contacts(request):
    return render(request, "main/contacts.html")


def contacts(request):
    return render(request, "main/sidebar.html")
