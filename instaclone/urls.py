from django.conf import  settings
from django.urls import path, re_path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name = 'home'),
    path('upload/image', views.upload_image, name = "upload_image"),
    path('create_profile/',views.create_profile,name = 'create_profile'),
    path('profile/<profile_id>',views.profile,name = 'profile'),
    path('like/<image_id>', views.like_image, name = 'like_image'),
    path('comment/<image_id>', views.comment,name = "comment"),
    path('profile/edit', views.update_profile,name = 'update_profile'),
    path('search/', views.search, name='search'),
    path('email/', views.email, name='email'),
    path('image/<image_id>',views.one_image,name = 'single_image')
        
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
