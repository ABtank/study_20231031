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
>  если стили не подгрузились то запуск сервера
```
python NewsStudyRTK/manage.py runserver --insecure
```
> [!NOTE]
> Связано с тем что DEGUB = False в настройках ([settings.py](NewsStudyRTK/NewsStudyRTK/settings.py) ) стоит 
> В документации написано, что обработка статики средствами Django - это очень медленно, небезопасно и допустимо к использованию только с dev-сервером в процессе разработки. В рабочем окружении статику должен обслуживать web-сервер.


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