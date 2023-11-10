from django.shortcuts import render
from django.http import HttpResponse
from .models import News
from .models import Product


def index(request):
    if request.method == "POST":
        print("POST")

        title = request.POST.get('product_title')
        price = request.POST.get('product_price')
        quantity = request.POST.get('product_quantity')
        new_product = Product(title, float(price), int(quantity))
        print('Создан товар:', new_product.title, 'Общая сумма:', new_product.amount())
        print(new_product, new_product.amount())
    else:
        print("GET")

    value = 0
    arr_numbers = ["раз", "два", "три"]
    new1 = News("Новость 1", "Текст 1", "07.11.23")
    new2 = News("Новость 2", "Текст 2", "08.11.23")
    new3 = News("Новость 3", "Текст 3", "09.11.23")
    arr_news = [new1, new2, new3]

    dictionary = {1: "один", 2: "два"}

    context = {"title": "Страница главная",
               "Header1": "Заголовок страницы",
               "value": value,
               "numbers": arr_numbers,
               "news": arr_news,
               "dictionary": dictionary,
               }

    colors = ['red', 'blue', 'golden', 'black']
    water = Product("water", 40, 2)
    chocolate = Product("chocolate", 50, 1)
    products = [water, chocolate]
    context['colors'] = colors
    context['products'] = products

    return render(request, "main/index.html", context)


def about(request):
    return render(request, "main/about.html")


def contacts(request):
    return render(request, "main/contacts.html")


def sidebar(request):
    return render(request, "main/sidebar.html")


# http://127.0.0.1:8000/calc/2/plus/3
def get_demo(request, a, operation, b):
    match operation:
        case 'plus':
            result = int(a) + int(b)
        case 'minus':
            result = int(a) - int(b)
        case 'multiply':
            result = int(a) * int(b)
        case 'divide':
            result = int(a) / int(b)
        case _:
            return HttpResponse(f'Вы ввели фигню')
    return HttpResponse(f'Вы ввели: {a} и {b} <br>результат {result}')


def custom_404(request, exception):
    return HttpResponse(f'<h1>404</h1> <br> {exception}')
