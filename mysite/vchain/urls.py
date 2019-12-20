from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('login', views.login, name='login'),
    path('create', views.create, name='create'),
    path('update', views.update, name='update')
]
