from django.shortcuts import render


# Create your views here.
def index(request):
    context = {}
    return render(request, "my_journal/index.html", context)


def full_width(request):
    context = {}
    return render(request, "my_journal/full-width.html", context)


def gallery(request):
    context = {}
    return render(request, "my_journal/gallery.html", context)


def portfolio(request):
    context = {}
    return render(request, "my_journal/portfolio.html", context)


def style_demo(request):
    context = {}
    return render(request, "my_journal/style-demo.html", context)
