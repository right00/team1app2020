from django.urls import path
from . import views

# set the application namespace
# https://docs.djangoproject.com/en/2.0/intro/tutorial03/
app_name = 'students'

urlpatterns = [

    path(r'', views.home, name = 'home'),
    path(r'task', views.task, name = 'task'),
    path(r'propose', views.propose, name = 'propose'),
    path(r'reserve', views.reserve, name = 'reserve'),
    path(r'tag', views.tag, name = 'tag'),

]
