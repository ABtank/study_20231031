from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import messages


def check_group(*groups):
    def decorator(function):
        def wrapper(request, *args, **kwargs):  # Функция-обёртка
            print('Декоратор сработал!', groups)
            user = request.user
            # если есть группы у нашего пользователя
            if user.groups.filter(name__in=groups).exists() or user.is_superuser or user.is_staff:
                print(*args)
                print(**kwargs)
                # то выполняем функцию-конфетку
                return function(request, *args, **kwargs)
            messages.warning(request, 'Нет доступа')
            # пересылаем пользователя туда, откуда он пришёл
            return HttpResponseRedirect(request.POST.get('next', '/'))

        return wrapper

    return decorator
