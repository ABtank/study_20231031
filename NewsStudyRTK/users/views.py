﻿import json

from django.contrib import messages
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group

from .forms import ContactForm, UserUpdateForm, AccountUpdateForm
from .models import *
from django.conf import settings

from news.models import Article
from my_news.models import MyArticle


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
        print('account_form.is_valid()', account_form.cleaned_data)
        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            messages.success(request, "Профиль успешно обновлен")
            return redirect('profile')
    else:
        context = {'account_form': AccountUpdateForm(instance=account),
                   'user_form': UserUpdateForm(instance=user)}
    return render(request, 'users/edit_profile.html', context)


def password_update(request):
    user = request.user
    form = PasswordChangeForm(user, request.POST)
    if request.method == 'POST':
        if form.is_valid():
            password_info = form.save()
            update_session_auth_hash(request, password_info)
            messages.success(request, 'Пароль успешно изменен')
            return redirect('profile')

    context = {"form": form}
    return render(request, 'users/edit_password.html', context)


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


@login_required
def add_to_favorites(request, article_id):
    article = Article.objects.get(id=article_id)
    # проверям есть ли такая закладка с этой новостью
    bookmark = FavoriteArticle.objects.filter(user=request.user.id,
                                              article=article)
    if bookmark.exists():
        bookmark.delete()
        messages.warning(request, f"Новость {article.title} удалена из закладок")
    else:
        bookmark = FavoriteArticle.objects.create(user=request.user, article=article)
        messages.success(request, f"Новость {article.title} добавлена в закладки")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def add_to_my_favorites(request, article_id):
    article = MyArticle.objects.get(id=article_id)
    # проверям есть ли такая закладка с этой новостью
    bookmark = MyFavoriteArticle.objects.filter(user=request.user.id,
                                                article=article)
    if bookmark.exists():
        bookmark.delete()
        messages.warning(request, f"Новость {article.title} удалена из закладок")
    else:
        bookmark = MyFavoriteArticle.objects.create(user=request.user, article=article)
        messages.success(request, f"Новость {article.title} добавлена в закладки")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def api_my_favorites(request):
    print('api_my_favorites')
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' \
            and request.method == 'POST' and request.POST.get('article_id', None) is not None:
        article_id = request.POST.get('article_id', None)
        print('article_id')
        article = MyArticle.objects.get(id=article_id)
        # проверям есть ли такая закладка с этой новостью
        bookmark = MyFavoriteArticle.objects.filter(user=request.user.id,
                                                    article=article)
        mes = {'text': f"Ошибка запроса", 'alert_class': 'danger'}
        exists = bookmark.exists()
        if exists:
            bookmark.delete()
            mes = {'text': f"Новость {article.title} удалена из избранного", 'alert_class': 'warning'}
        else:
            bookmark = MyFavoriteArticle.objects.create(user=request.user, article=article)
            mes = {'text': f"Новость {article.title} добавлена в избранное", 'alert_class': 'success'}

        response = {'mes': mes, 'article_id': article_id, 'bookmark': not exists}

        return JsonResponse(response, status=200)

    return JsonResponse({'error': 'Ошибка запроса'}, status=401)


@login_required
def api_thumbs_article(request):
    print('api_thumbs_article')
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' \
            and request.method == 'POST' and request.POST.get('article_id', None) is not None:
        article_id = request.POST.get('article_id', None)
        rating = request.POST.get('rating', 0)
        print('article_id=', article_id,article_id is not None, 'rating=', rating,rating in ['-1', '0', '1'])
        if article_id is not None and int(rating) in [-1, 0, 1]:
            article = MyArticle.objects.get(id=article_id)
            print('article',article)
            thumbs = MyHandThumbsArticle.objects.filter(user=request.user.id, article=article).first()
            print('thumbs',thumbs)
            if thumbs is None:
                MyHandThumbsArticle.objects.create(user=request.user, article=article, rating=rating)
                mes = {'text': f"Новость {article.title} оценка {rating} учтена", 'alert_class': 'info'}
            else:
                if int(rating) == 0:
                    thumbs.delete()
                    mes = {'text': f"Новость {article.title} оценка удалена", 'alert_class': 'info'}
                else:
                    thumbs.rating = rating
                    thumbs.save()
                    mes = {'text': f"Новость {article.title} оценка {rating} учтена", 'alert_class': 'info'}

            response = {'mes': mes, 'article_id': article_id, 'rating': rating}
            return JsonResponse(response, status=200)

    return JsonResponse({'error': 'Ошибка запроса'}, status=401)
