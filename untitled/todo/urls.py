from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings
from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.pagelogout, name='logout'),
    path('loggedin/upload/',views.upload,name='upload'),
    path('loggedin/files/', views.files, name='files'),
    path('delete/<str:usr>/<int:tid>/',views.delete,name='delete'),
    path('edit/<str:usr>/<int:tid>/',views.edit,name='edit'),
    path('status/<str:sta>/<str:usr>/<int:tid>/',views.status1,name='status1'),
    path('contact/', views.contact, name='contact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)