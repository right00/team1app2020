from django.contrib import admin
from . import models 

admin.site.register(models.Base)
admin.site.register(models.Teachers)
admin.site.register(models.Students)
admin.site.register(models.Classes)
admin.site.register(models.Tags)
admin.site.register(models.Tasks)
admin.site.register(models.StudentTasks)
admin.site.register(models.Schedule)
admin.site.register(models.ScheduleData)
admin.site.register(models.Question)
admin.site.register(models.AppoTime)
admin.site.register(models.Accept)
admin.site.register(models.Comment)

#from .models import User, Entry

"""
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Entry)
class Entry(admin.ModelAdmin):
    pass
"""