from django.conf import Settings, settings
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.welcome, name='welcome'),
]

if Settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
