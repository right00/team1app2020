from django.urls import path
from . import views

# set the application namespace
# https://docs.djangoproject.com/en/2.0/intro/tutorial03/
app_name = 'teachers'

urlpatterns = [
    path('class/',views.edit_class,name = 'teclass'),
]