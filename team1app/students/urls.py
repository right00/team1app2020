from django.urls import path
from . import views

from django.conf.urls import url
from django.contrib import admin


# set the application namespace
# https://docs.djangoproject.com/en/2.0/intro/tutorial03/
app_name = 'students'

urlpatterns = [

    path('', views.home, name = 'home'),
    path('home/<int:classid>', views.class_page, name = "class_page"), 
    path('home/task/', views.task, name = 'task'),
    path('home/propose/', views.propose, name = 'propose'),
    path('home/reserve/', views.reserve, name = 'reserve'),
    path('home/tag/', views.tag, name = 'tag'),


]
