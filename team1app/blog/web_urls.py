from django.urls import path
from . import web_views_public as pub
from . import web_views_private as priv

urlpatterns = [
    path('', pub.top, name = 'top'),
    path('home/', priv.home, name = 'home'),
    path('home/task', priv.task, name = 'task'),
    path('home/propose', priv.propose, name = 'propose'),
    path('home/reserve', priv.reserve, name = 'reserve'),
    path('home/tag', priv.tag, name = 'tag')


]
