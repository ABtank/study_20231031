from django.contrib import messages
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group

from .forms import ContactForm, UserUpdateForm, AccountUpdateForm
from .models import *
from django.conf import settings


def profile(request):
    context = dict()
    return render(request, 'users/profile.html', context)

def profile_update(request):
    user = request.user
    account = Account.objects.filter(user=user).first()
    if account is None:
        account = Account(user.id)
        account.save()
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=user)
        account_form = AccountUpdateForm(request.POST, request.FILES, instance=account)
        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            messages.success(request,"Профиль успешно обновлен")
            return redirect('profile')
    else:
        context = {'account_form':AccountUpdateForm(instance=account),
                   'user_form':UserUpdateForm(instance=user)}
    return render(request,'users/edit_profile.html',context)


def password_update(request):
    user = request.user
    form = PasswordChangeForm(user,request.POST)
    if request.method == 'POST':
        if form.is_valid():
            password_info = form.save()
            update_session_auth_hash(request,password_info)
            messages.success(request,'Пароль успешно изменен')
            return redirect('profile')

    context = {"form": form}
    return render(request,'users/edit_password.html',context)

@login_required(login_url=settings.LOGOUT_REDIRECT_URL)
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


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # появляется новый пользователь
            group = Group.objects.get(name="Authors")
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            authenticate(username=username, password=password)
            # создаем пустой аккаунт
            acc = Account(user.id)
            acc.save()
            messages.success(request, f'{username} был зарегистрирован!')
            return redirect('news_list')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)
