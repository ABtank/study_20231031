from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render

from .forms import ContactForm
from .models import *


def contact_page(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print('Сообщение отправлено', form.cleaned_data)  # form.cleaned_data = json
            messages.success(request, f'Сообщение отправлено "{form.cleaned_data}"!')
        else:
            print(form.errors)
            messages.error(request, form.errors)
            for err in form.errors:
                messages.error(request, form.errors.get(err))
                print(form.errors.get(err))
    else:
        form = ContactForm()
        form.name = 'Любимый клиент'
    context = {'form': form}
    return render(request, 'users/contact_page.html', context)


def index(request):
    print(request.user, request.user.id)

    user_acc = Account.objects.get(user=request.user)
    print(user_acc, user_acc.nickname, user_acc.birthdate, user_acc.gender)
    return HttpResponse("Приложение Users")
