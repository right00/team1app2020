from . import views
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

# set the application namespace
# https://docs.djangoproject.com/en/2.0/intro/tutorial03/
app_name = 'teachers'

urlpatterns = [
    path('class/',views.edit_class,name='teclass'),
    path('create_class/',views.create_class,name='CreateClass'),
    path('class/<int:classid>/',views.class_content,name='ClassContent'),
    path('class/<int:classid>/task/create/',views.create_task,name='CreateTask'),
    path('class/<int:classid>/tasks/',views.TasksList,name='TasksList'),
    path('class/<int:classid>/task/<int:taskid>/',views.taskContent,name="taskContent"),
    path('class/<int:classid>/tags/',views.edit_tags),
    path('class/<int:classid>/st/<int:studentid>/',views.studentContents),

    path('schedule/',views.schedule),
    path('questions/',views.questions,name="questions"),
    path('questions/<int:id>/',views.question),
    
]
