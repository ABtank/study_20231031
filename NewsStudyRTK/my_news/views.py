import json
import random

from django.contrib import messages
from django.contrib.auth import authenticate, update_session_auth_hash, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView

from .forms import MyArticleForm, ImagesFormSet
from .models import MyTag, MyArticle, User, MyImage, MyViewCount
from users.models import Account

from users.forms import AccountUpdateForm, UserUpdateForm

from .utils import get_client_ip


class MyArticleUpdateView(UpdateView):
    model = MyArticle
    template_name = 'my_news/create_article.html'
    fields = ['title', 'anouncement', 'text', 'tags']

    def get_context_data(self, **kwargs):
        context = super(MyArticleUpdateView, self).get_context_data(**kwargs)
        current_object = self.object
        context['image_form'] = ImagesFormSet(instance=current_object)
        return context

    def post(self, request, **kwargs):
        print(request.POST)
        request.POST = request.POST
        current_object = MyArticle.objects.get(id=request.POST['myimage_set-0-article'])
        deleted_ids = []
        for i in range(int(request.POST['myimage_set-TOTAL_FORMS'])):  # удаление всех по галочкам
            field_delete = f'myimage_set-{i}-DELETE'
            field_image_id = f'myimage_set-{i}-id'
            if field_delete in request.POST and request.POST[field_delete] == 'on':
                image = MyImage.objects.get(id=request.POST[field_image_id])
                image.delete()
                deleted_ids.append(field_image_id)

                # тут же удалить картинку из request.FILES
        # Замена картинки
        for i in range(int(request.POST['myimage_set-TOTAL_FORMS'])):  # удаление всех по галочкам
            field_replace = f'myimage_set-{i}-image'  # должен быть в request.FILES
            field_image_id = f'myimage_set-{i}-id'  # этот файл мы заменим
            if field_replace in request.FILES and request.POST[
                field_image_id] != '' and field_image_id not in deleted_ids:
                image = MyImage.objects.get(id=request.POST[field_image_id])  #
                image.delete()  # удаляем старый файл
                for img in request.FILES.getlist(field_replace):  # новый добавили
                    MyImage.objects.create(article=current_object, image=img, title=img.name)
                del request.FILES[field_replace]  # удаляем использованный файл
        if request.FILES:  # Добавление нового изображения
            print('!!!!!!!!!!!!!!!!!', request.FILES)
            for input_name in request.FILES:
                for img in request.FILES.getlist(input_name):
                    print('###############', img)
                    MyImage.objects.create(article=current_object, image=img, title=img.name)
        messages.info(request, f'Обновлена статья  №{current_object.id} - "{current_object.title}"!')
        return super(MyArticleUpdateView, self).post(request, **kwargs)


class MyArticleDeleteView(DeleteView):
    model = MyArticle
    success_url = reverse_lazy('my_news')
    template_name = 'my_news/delete_article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_object = self.object
        images = MyImage.objects.filter(article=current_object)
        context['images'] = images
        return context


def generate_random_list(input_list):
    random_length = random.randint(0, len(input_list))
    random_items = random.sample(input_list, random_length)
    return random_items


def random_article(target):
    list_tags = MyTag.objects.all().values_list('id', flat=True)
    random_tag_ids = generate_random_list(list(list_tags))
    random_tags = MyTag.objects.filter(id__in=random_tag_ids)
    len_text = random.randint(100, 500)
    numb = MyArticle.objects.count() + 1
    authors = User.objects.all()
    num_acc = random.randint(0, len(authors) - 1)
    author = authors[num_acc]
    article = MyArticle(author=author, title=f"title-{target} {numb}",
                        anouncement=(f"Анонс-{target} {numb}" * (len_text // 5))[:250],
                        text=f"{target} {numb} " * len_text,
                        category=get_category())
    article.save()
    article.tags.set(random_tags)
    article.save()
    return article


def get_category():
    category = [category[0] for category in MyArticle.categories]
    random_number = random.randint(0, len(category) - 1)
    return category[random_number]


# Create your views here.
def index(request):
    context = {}
    return render(request, "my_news/index.html", context)


def publication(request, target):
    random_article(target)
    context = {}
    tags_list = (MyTag.objects
                 .annotate(num_articles=Count('myarticle'))
                 .all())
    authors_list = User.objects.annotate(Count('myarticle', distinct=True))
    context['tags_list'] = tags_list
    context['authors_list'] = authors_list

    # Фильтр
    search = ''
    tags_selected = []
    if target in [category[0] for category in MyArticle.categories]:
        categories_selected = target
    else:
        categories_selected = []
    authors_selected = []
    filters = Q()  # Создаем пустой объект Q

    if request.session.get('filters') is not None:
        session_filter = request.session.get('filters')
    else:
        session_filter = {}

    is_filtered = False
    if request.method == "POST":
        if request.session.get('filters', None) is not None:
            del request.session['filters']
        if request.POST.get('clear_filter') is None:
            tags_selected = [int(tag_id) for tag_id in request.POST.getlist('tags_filter') if len(tag_id) > 0]
            if len(tags_selected) > 0:
                session_filter['tags_filter'] = tags_selected
            authors_selected = [int(author_id) for author_id in request.POST.getlist('authors_filter') if
                                len(author_id) > 0]
            if len(authors_selected) > 0:
                session_filter['authors_filter'] = authors_selected

            if len(request.POST.getlist('categories_filter')) > 0:
                session_filter['categories_filter'] = request.POST.getlist('categories_filter')

            search = request.POST.get('search_news')
            if search is not None and len(search) > 0:
                session_filter['search_news'] = search
            else:
                search = ''
            request.session['filters'] = session_filter

    if request.session.get('filters') is not None:
        is_filtered = True
        if session_filter.get('tags_filter', None) is not None:
            tags_selected = session_filter['tags_filter']
            filters &= Q(tags__in=tags_selected)
        if session_filter.get('authors_filter', None) is not None:
            authors_selected = session_filter['authors_filter']
            filters &= Q(author__in=authors_selected)
        if session_filter.get('categories_filter', None) is not None:
            categories_selected = session_filter['categories_filter']
            filters &= Q(category__in=categories_selected)
        if session_filter.get('search_news', None) is not None:
            search = session_filter['search_news']
            filters &= (Q(title__icontains=search) | Q(anouncement__icontains=search))

    if target == "my":
        filters &= Q(author=request.user.id)
        print(target)

    if not is_filtered and target in [category[0] for category in MyArticle.categories]:
        filters &= Q(category__iexact=target)

    match target:
        case 'hot' | 'fresh' | 'best' | 'my':
            articles = (MyArticle.objects
                        .select_related("author")
                        .prefetch_related('tags')
                        .annotate(Count('tags'))
                        .filter(filters)
                        .order_by('-id')
                        .all())
        case _:
            return render(request, "my_news/custom_404.html", {'exception': "страница не найдена"})

    paginator = Paginator(articles, 10)  # здесь 10 - это количество элементов на одну страницу
    page_number = request.GET.get('page')  # номер страницы, полученный из запроса
    page_articles = paginator.get_page(page_number)

    print(filters)

    context['target'] = target
    context['articles'] = page_articles
    context['tags_list'] = tags_list
    context['tags_selected'] = tags_selected
    context['categories_list'] = MyArticle.categories
    context['categories_selected'] = categories_selected
    context['authors_selected'] = authors_selected
    context['is_filtered'] = is_filtered
    context['search_news'] = search
    context['articles_count'] = articles.count()
    return render(request, "my_news/publication.html", context)


def article(request, article_id, mode):
    context = {}

    article = (MyArticle.objects
               .select_related("author")
               .prefetch_related('tags')
               .annotate(Count('tags'))
               .filter(id=article_id)
               .first())
    if article is None:
        messages.error(request, "Статья не найдена!")
        return redirect('publication', target='fresh')

    context["article"] = article
    match mode:
        case 'view':
            print('view')
            MyViewCount.objects.get_or_create(article=article, ip_address=get_client_ip(request))
        case 'edit':
            if request.method == "POST":
                print("POST")
                form = MyArticleForm(request.POST, instance=context["article"], files=request.FILES)
                print(form.changed_data)
                current_user = request.user
                if current_user.id is not None:  # проверили что не аноним
                    new_article = form.save()
                    new_article.author = current_user
                    new_article.save()  # сохраняем в БД
                    for img in request.FILES.getlist('image_field'):
                        MyImage.objects.create(article=new_article, image=img, title=img.name)
                    messages.info(request, f'Обновлена статья  №{article_id} - "{new_article.title}"!')
                    context["article"] = (MyArticle.objects
                                          .select_related("author")
                                          .prefetch_related('tags')
                                          .annotate(Count('tags'))
                                          .get(id=new_article.id))
                    return redirect('article', article_id=article_id, mode='view')
                else:
                    messages.error(request, "Не авторизованы")
            else:
                print('edit GET')
                context["form"] = MyArticleForm(instance=context["article"])
        case _:
            return render(request, "my_news/custom_404.html", {'exception': "страница не найдена"})
    print(context)
    return render(request, "my_news/article.html", context)


@login_required(login_url="my_news")
def create_my_article(request):
    if request.method == 'POST':
        form = MyArticleForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            if current_user.id is not None:  # проверили что не аноним
                new_article = form.save(commit=False)  # сохранение без коммита
                new_article.category = get_category()  # рандомно устанавливаем категорию
                new_article.save()  # сохраняем в БД
                new_article.author = current_user
                new_article.save()  # сохраняем в БД
                form.save_m2m()
                for img in request.FILES.getlist('image_field'):
                    MyImage.objects.create(article=new_article, image=img, title=img.name)
                messages.info(request, f"Создана новая статья №{new_article.id} - {new_article.title}")
                messages.info(request, f"Поздравляем! Ваша статья попала в раздел {new_article.category}!", 'primary')
                if request.POST.get('saveAndNew') is not None:
                    form = MyArticleForm()
                else:
                    return redirect(f'article/{new_article.id}/view')
            else:
                messages.error(request, "Не авторизованы")
    else:
        form = MyArticleForm()
    return render(request, 'my_news/create_article.html', {'form': form})


def info(request):
    context = {}
    return render(request, "my_news/info.html", context)


# def signIn(request):
#     context = {}
#     return render(request, "my_news/sign-in.html", context)

def my_registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # появляется новый пользователь
            group = Group.objects.get(name='Authors')
            user.groups.add(group)

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            # !!!не аутентифицируется - нужно доделать
            authenticate(username=username, password=password)
            # создаем пустой аккаунт
            acc = Account(user.id)
            acc.save()
            # залогинить
            login(request, user)
            messages.success(request, f'{username} был зарегистрирован!', 'info')
            return redirect('my_profile')
            # return redirect('sing_in')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'my_news/my_registration.html', context)


@login_required(login_url="my_news")
def my_profile(request):
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
            messages.info(request, "Профиль успешно обновлен")
        else:
            messages.error(request, "Профиль обновить не удалось", 'danger')
    count_my_articles = MyArticle.objects.filter(author=user).count()
    count_hot_articles = MyArticle.objects.filter(author=user, category__iexact='hot').count()
    count_fresh_articles = MyArticle.objects.filter(author=user, category__iexact='fresh').count()
    count_best_articles = MyArticle.objects.filter(author=user, category__iexact='best').count()
    context = {'account_form': AccountUpdateForm(instance=account),
               'user_form': UserUpdateForm(instance=user),
               'count_my_articles': count_my_articles,
               'count_hot_articles': count_hot_articles,
               'count_fresh_articles': count_fresh_articles,
               'count_best_articles': count_best_articles,
               }
    return render(request, 'my_news/profile.html', context)


def password_update(request):
    user = request.user
    form = PasswordChangeForm(user, request.POST)
    if request.method == 'POST':
        if form.is_valid():
            password_info = form.save()
            update_session_auth_hash(request, password_info)
            messages.success(request, 'Пароль успешно изменен')
            return redirect('profile')


def custom_404(request, exception):
    context = {'exception': exception}
    return render(request, "my_news/custom_404.html", context)


def search_news(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        q = request.GET.get('term', '')
        articles = MyArticle.objects.filter(title__icontains=q)
        results = []
        for a in articles:
            results.append(a.title)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
