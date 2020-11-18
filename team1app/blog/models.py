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
#教師
class Teachers(models.Model):
    name = models.CharField(max_length=32)
    person = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=None)
    use_base = models.IntegerField(default=None,null=True,blank=True)
#生徒
class Students(models.Model):
    name = models.CharField(max_length=32)
    person = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=None)
    use_base = models.IntegerField(default=None,null=True,blank = True)
    
    def getHomework(self):
        return self.studenttasks_set.all()
    
    def getHomeworkT(self,teacher):
        hws = []
        for hw in self.studenttasks_set.all():
            for t in hw.task.all():
                for a in t.auther.all():
                    if(a == teacher):
                        hws.append(hw)
                        break
        return hws

#学校    
class Base(models.Model):
    base_name = models.CharField(max_length=128)
    #先生用
    password = models.CharField(max_length=32,default="0000")
    #生徒用
    password2 = models.CharField(max_length=32,default="1111")
    #管理者
    administrator = models.ManyToManyField(settings.AUTH_USER_MODEL)
    #在籍する教師
    teachers = models.ManyToManyField(Teachers)
    #在籍する生徒
    students = models.ManyToManyField(Students,blank=True)

#クラス関係

#クラス
class Classes(models.Model):
    #クラスの名前
    class_name=models.CharField(max_length=32)
    #所属するbase
    base = models.ForeignKey(Base,on_delete=models.CASCADE)
    #クラスのパスワード
    password = models.CharField(max_length=32,default=0000)
    #在籍する教師
    teachers = models.ManyToManyField(Teachers)
    #在籍する生徒
    students = models.ManyToManyField(Students,blank=True)

#タグ
class Tags(models.Model):
    #タグの名前
    tag = models.CharField(max_length=32)
    #タグのあるクラス
    tarclass = models.ForeignKey(Classes,on_delete=models.CASCADE)

#宿題
class Tasks(models.Model):
    #宿題の名前
    name = models.CharField(max_length=32)
    #宿題の内容
    contents = models.TextField()
    #作った人
    auther = models.ManyToManyField(Teachers)
    #宿題につけられたタグ
    tag = models.ManyToManyField(Tags,blank=True)
    #タグが置かれたクラス
    tarclass = models.ForeignKey(Classes,on_delete=models.CASCADE)
    #作られた日付
    make = models.DateField(default=timezone.now)

#生徒に出された宿題
class StudentTasks(models.Model):
    #出された宿題
    task = models.ManyToManyField(Tasks)
    #期限
    limit = models.DateField()
    #終わったかどうか
    finish = models.BooleanField(default=False)
    #宿題の正誤
    result = models.BooleanField(default=False)
    #出された人
    person = models.ForeignKey(Students,on_delete=models.CASCADE)

    
    



    