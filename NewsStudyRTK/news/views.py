from django.shortcuts import render


def index(request):
    return render(request, "news/index.html")


# def news(request):
#     return render(request, "news/news.html")
