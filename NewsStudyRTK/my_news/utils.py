from .models import MyViewCount


def get_client_ip(request):
    print("get_client_ip")
    x_forwrded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwrded_for:
        print(x_forwrded_for)
        ip = x_forwrded_for.split(',')[0]
    else:
        print(request.META.get('REMOTE_ADDR'))
        ip = request.META.get('REMOTE_ADDR')
    return ip
