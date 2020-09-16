from django.db import models
from django.conf import settings
from django.utils import timezone

"""
class User(models.Model):
    name = models.CharField(max_length=32)
    mail = models.EmailField()
    def __repr__(self):
        # 主キーとnameを表示させて見やすくする
        # ex) 1: Alice
        return "{}: {}".format(self.pk, self.name)

    __str__ = __repr__  # __str__にも同じ関数を適用


class Entry(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_PUBLIC = "public"
    STATUS_SET = (
            (STATUS_DRAFT, "下書き"),
            (STATUS_PUBLIC, "公開中"),
    )
    title = models.CharField(max_length=128)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_SET, default=STATUS_DRAFT, max_length=8)
    author = models.ForeignKey(User, related_name='entries', on_delete=models.CASCADE)
"""
class Base(models.Model):
    base_name = models.CharField(max_length=128)
    administrator = models.ManyToManyField(settings.AUTH_USER_MODEL)

class Teachers(models.Model):
    name = models.CharField(max_length=32)
    person = models.ManyToManyField(settings.AUTH_USER_MODEL)
    base = models.ForeignKey(Base,on_delete=models.CASCADE)

class Students(models.Model):
    name = models.CharField(max_length=32)
    person = models.ManyToManyField(settings.AUTH_USER_MODEL)
    base = models.ForeignKey(Base,on_delete=models.CASCADE)
#クラス関係

class Classes(models.Model):
    class_name=models.CharField(max_length=32)
    base = models.ForeignKey(Base,on_delete=models.CASCADE)

class ClassTeachers(models.Model):
    person = models.ManyToManyField(Teachers)
    tarclass = models.ForeignKey(Classes,on_delete=models.CASCADE)

class ClassStudents(models.Model):
    person = models.ManyToManyField(Students)
    tarclass = models.ForeignKey(Classes,on_delete=models.CASCADE)

class Tags(models.Model):
    tag = models.CharField(max_length=32)
    tarclass = models.ForeignKey(Classes,on_delete=models.CASCADE)

class Tasks(models.Model):
    name = models.CharField(max_length=32)
    contents = models.TextField()
    tag = models.ManyToManyField(Tags)
    tarclass = models.ForeignKey(Classes,on_delete=models.CASCADE)

#教師関係
class TeacherClasses(models.Model):
    classmodel = models.ManyToManyField(Classes)
    person = models.ForeignKey(Teachers,on_delete=models.CASCADE)

#生徒関係
class StudentClasses(models.Model):
    classmodel = models.ManyToManyField(Classes)
    person = models.ForeignKey(Teachers,on_delete=models.CASCADE)

class StudentTasks(models.Model):
    task = models.ManyToManyField(Tasks)
    limit = models.DateField()
    finish = models.BooleanField(default=False)
    result = models.BooleanField(default=False)
    person = models.ForeignKey(Teachers,on_delete=models.CASCADE)

    


    



    