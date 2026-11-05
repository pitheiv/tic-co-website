from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from .views import home, menu

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('menu/', menu, name='menu'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]