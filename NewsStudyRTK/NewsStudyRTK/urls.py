"""
URL configuration for NewsStudyRTK project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

# Для проверки своей страницы 404, конфигурация такая:
# import main.views as main_views
# handler404 = main_views.custom_404
import my_news.views as my_news_views
handler404 = my_news_views.custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('shop/', include('shop.urls')),
    path('my_journal/', include('my_journal.urls')),
    path('my_news/', include('my_news.urls')),
    path('news/', include('news.urls')),
    path('users/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug/__', include(debug_toolbar.urls)),
                  ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
