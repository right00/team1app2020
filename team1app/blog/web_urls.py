from django.urls import path
from . import web_views_public as pub
from . import web_views_private as priv

urlpatterns = [
path('', pub.top , name='top'),
path('NewGroup/',priv.makegroup,name='newgroup'),
path('join/',priv.signincrassroom,name = 'join'),
]
