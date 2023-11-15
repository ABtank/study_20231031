from django.shortcuts import render


# Create your views here.
def index(request):
    context = {}
    return render(request, "my_news/index.html", context)


def publication(request, target):
    context = {"target": target}
    return render(request, "my_news/publication.html", context)


def article(request):
    context = {}
    return render(request, "my_news/article.html", context)


def profile(request):
    context = {}
    return render(request, "my_news/profile.html", context)


def info(request):
    context = {}
    return render(request, "my_news/info.html", context)


def signIn(request):
    context = {}
    return render(request, "my_news/sign-in.html", context)