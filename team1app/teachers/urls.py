from . import views
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

# set the application namespace
# https://docs.djangoproject.com/en/2.0/intro/tutorial03/
app_name = 'teachers'

urlpatterns = [
    path('',views.edit_class,name='teclass'),
    path('create_class/',views.create_class,name='CreateClass'),
]