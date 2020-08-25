"""team1app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from blog import views as blog_views

from blog.urls import router as blog_router
from django.urls import path



urlpatterns = [

    path('top',blog_views.top, name = 'top'),
    path('home',blog_views.home, name = 'home'),
    path('home/task',blog_views.Atask, name = 'task'),
    path('home/purpose',blog_views.Bpurpose, name = 'purpose'),
    path('home/reserve',blog_views.Creserve, name = 'reserve'),
    path('home/tag',blog_views.Dtag, name = 'tag'),
    path('home/rec',blog_views.Erec, name = 'rec'),
    path(r'admin/', admin.site.urls),
    path(r'api/', include(blog_router.urls)),
]
