# study_20231031

Навигация
-----------

- [Корневой урл](http://127.0.0.1:8000/) - в ней будут ссылки на все остальные проекты
- [my_journal](http://127.0.0.1:8000/my_journal/) - первая попытка шаблона
- [my_news](http://127.0.0.1:8000/my_news/) - шаблон на проверку ДЗ №1
- [shop](http://127.0.0.1:8000/my_news/) - шаблон магазина с лекций

Установка
------------

### ! Все команды выполнять в корне проекта

> [!WARNING]
> Могут быть проблемы с версией python 3.12

1) лечение

```
  python -m ensurepip --upgrade
```

2) Запуск виртуальной среды из корневой папки

```
venv/Scripts/activate
```

> [!NOTE]
> Если ошибка и нет папки venv

```
python -m venv venv
```

3) Установка необходимых библиотек (pip3, просто pip не прокатит)

```
pip3 install -r requirements.txt
```

4) Запуск сервера

```
python NewsStudyRTK/manage.py runserver
```

> [!WARNING]
> если стили не подгрузились то запуск сервера

```
python NewsStudyRTK/manage.py runserver --insecure
```

> [!NOTE]
> Связано с тем что DEGUB = False в настройках ([settings.py](NewsStudyRTK/NewsStudyRTK/settings.py) ) стоит
> В документации написано, что обработка статики средствами Django - это очень медленно, небезопасно и допустимо к
> использованию только с dev-сервером в процессе разработки. В рабочем окружении статику должен обслуживать web-сервер.


Что реализовано к ДЗ №1 [Новости](http://127.0.0.1:8000/my_news/)
------------

1) [x] Шаблон для главной страницы
2) [x] Шаблон для отдельной страницы новости (чтение/создание/редактирование)
3) [x] Шаблон страницы со списком новостей
4) [x] Страница аккаунта пользователя
5) [x] Шаблон для навигации верхняя и боковая панель
6) [x] Шаблон 404
7) [x] Шаблон логина

## Администрирование

1) инициализация БД

```
python .\NewsStudyRTK\manage.py migrate
```

2) создание пользователя

```
python .\NewsStudyRTK\manage.py createsuperuser
```

## Миграциии

1) подготовка к обновлению

```
python .\NewsStudyRTK\manage.py makemigrations
```

2) обновление БД

```
python .\NewsStudyRTK\manage.py migrate
```

3) работа с картинками (Pillow)

```
pip install Pillow
```

4) работа с БД из консоли с ORM

``` 
python .\NewsStudyRTK\manage.py shell 
```

5) django-debug-toolbar

```
python -m pip install django-debug-toolbar
```

### Формы

1) crispy

```
python -m pip install django-crispy-forms
 ```

2) crispy-bootstrap5

```
python -m pip install crispy-bootstrap5
 ```

### Переход на Postgres

1) Установка необходимых библиотек
   для сохранения ключей в окружении

 ```
pip install django-environ
```

для работы с БД

 ```
pip install psycopg2
```

Для MacOS

 ```
pip install psycopg2-binary 
```

дамп БД из sqlite

``` 
python manage.py dumpdata > data.json
```

либо лучше

```
python .\NewsStudyRTK\manage.py dumpdata --indent=2 -o  data.json
```

создаем пустую структуру в новой БД

```
python .\NewsStudyRTK\manage.py migrate
```

удаляем все записи миграции
выполняем создание новых миграций
делаем миграцию
чистим типы данных чтоб не было конфликтов в типах

```
python .\NewsStudyRTK\manage.py shell
```

```
from django.contrib.contenttypes.models import ContentType
```

``` 
ContentType.objects.all().delete()
```

``` 
quit()
```

загружаем дамп старой БД

``` 
python .\NewsStudyRTK\manage.py loaddata .\data.json
```

если че не получается то скорей всего кодировка файла data.json не UTF-8

## Опубликован на https://abtank.pythonanywhere.com/my_news/

### Публикация на www.pythonanywhere.com

в баш устанавливаем виртуальную среду

```
mkvirtualenv --python=/usr/bin/python3.10 first_study
```

```
pip3 install -r requirements.txt
```

```
python manage.py migrate
```

#### Web

1) Code:
    1) Source code: /home/abtank/study_20231031

    2) Working directory: /home/abtank/

    3) WSGI configuration file:/var/www/abtank_pythonanywhere_com_wsgi.py
       1) в файле прописываем
         ```
            import os
            import sys
            path = '/home/abtank/study_20231031/NewsStudyRTK/'
            if path not in sys.path:
                sys.path.append(path)
            
            os.environ['DJANGO_SETTINGS_MODULE'] = 'NewsStudyRTK.settings'
            
            from django.core.wsgi import get_wsgi_application
            application = get_wsgi_application()
         ```
    4) Python version: 3.10
2) Static files:
   1) /media/	/home/abtank/study_20231031/NewsStudyRTK/media
   2) /static/	/home/abtank/study_20231031/NewsStudyRTK/my_news/static	

#### FILE
1) settings.py
   2) ALLOWED_HOSTS = ['abtank.pythonanywhere.com']