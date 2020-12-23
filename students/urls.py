from django.urls import path, re_path
from . import views,test

from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static


# set the application namespace
# https://docs.djangoproject.com/en/2.0/intro/tutorial03/
app_name = 'students'

urlpatterns = [

    path('', views.home, name = 'home'),
    path('home/<int:class_id>/', views.class_page, name = "class_page"), 
    path('home/task/', views.task, name = 'task'),
    path('home/propose/', views.propose, name = 'propose'),
    path('home/tag/', views.tag, name = 'tag'),

    path('home/chat/<int:id>/', views.room, name = 'room'),
    path('home/chat/', views.chat, name = 'chat'),
    path('home/chat/create/', views.chat_create, name = 'chat_create'),

]
