from django.shortcuts import render


# Create your views here.
def index(request):
    context = {"title": "Страница главная",
               "Header1": "Заголовок страницы",
               }
    return render(request, "shop/index.html", context)
