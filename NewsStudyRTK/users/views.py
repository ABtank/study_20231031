from django.http import HttpResponse
from .models import *


def index(request):
    print(request.user, request.user.id)

    user_acc = Account.objects.get(user=request.user)
    print(user_acc, user_acc.nickname, user_acc.birthdate, user_acc.gender)
    return HttpResponse("Приложение Users")
