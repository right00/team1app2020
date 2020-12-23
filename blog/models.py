from django.db import models
from django.conf import settings
from django.utils import timezone
import re

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

    def getQuestions(self):
        result = None
        if(Question.objects.filter(toTe = self).exists):
            result = Question.objects.filter(toTe = self)
        return result

#生徒
class Students(models.Model):
    name = models.CharField(max_length=32)
    person = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=None)
    use_base = models.IntegerField(default=None,null=True,blank = True)
    
    def getQuestions(self):
        result = None
        if(Question.objects.filter(fromSt = self).exists):
            result = Question.objects.filter(fromSt = self)
        return result

    def getHomework(self):
        return self.studenttasks_set.all()

    def getClassHomework(self,Class):
        result = []
        for homework in self.studenttasks_set.all():
            if(homework.task.all()[0].tarclass == Class):
                result.append(homework)
        return result

    def getMyClassHomework(self):
        result = []
        if(Classes.objects.filter(students = self).exists()):
            cs = Classes.objects.filter(students = self)
            for c in cs:
                data = {"class":c,"homeworks":self.getClassHomework(c)}
                result.append(data)

        return result

    
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
    #正解があるかどうか
    isResult = models.BooleanField(default=False, blank=True, null=True)
    #宿題の正誤
    result = models.BooleanField(default=False)
    #出された人
    person = models.ForeignKey(Students,on_delete=models.CASCADE)

    def getIsResult(self):
        if self.isResult == null:
            return True
        else:
            return self.isResult 

class Schedule(models.Model):
    person = models.ForeignKey(Teachers,on_delete=models.CASCADE)

    def add(self,week,start_h,start_m,end_h,end_m):
        data = None
        datas = self.getScheduleData()
        if(datas != None):
            if(datas[week] != None):
                for i in datas[week]['data']:
                    sh,sm = i.getStartInt()
                    eh,em = i.getEndInt()

                    if(start_h < sh or (start_h == sh and start_m < sm)):
                        if(end_h < sh or (end_h == sh and end_m < sm)):
                            continue

                        elif(start_h < sh or (start_h == sh and start_m < sm)):
                            i.start="{:0>2}:{:0>2}".format(str(start_h),str(start_m))
                            if(data != None):
                                data.delete()
                            data = i
                            data.save()
                            end_h = eh
                            end_m = em
                            continue

                        else:
                            i.start="{:0>2}:{:0>2}".format(str(start_h),str(start_m))
                            i.end="{:0>2}:{:0>2}".format(str(end_h),str(end_m))
                            if(data != None):
                                data.delete()
                            data = i
                            data.save()
                            continue

                    elif(start_h < eh or (start_h == eh and start_m <= sm)):
                        if(start_h < sh or (start_h == sh and start_m < sm)):
                            data = i
                            break

                        else:
                            i.end="{:0>2}:{:0>2}".format(str(end_h),str(end_m))
                            if(data != None):
                                data.delete()
                            data = i
                            data.save()
                            start_h = eh
                            start_m = em
                            continue

                    else:
                        continue
        if(data == None):
            data = ScheduleData.objects.create(schedule = self,start = "{:0>2}:{:0>2}".format(start_h,start_m),end = "{:0>2}:{:0>2}".format(end_h,end_m))
            data.save()
        
        return 0

    def getScheduleData(self):
        strweek = "月火水木金土日"
        lst = None
        if(ScheduleData.objects.filter(schedule = self).exists()):
            scheduledatas = ScheduleData.objects.filter(schedule = self)
            lst = []
            for i in range(7):
                if(scheduledatas.filter(week = i).exists()):
                    d = scheduledatas.filter(week = i)
                    data = {"data":d,"weekstr":strweek[i]}
                    lst.append(data)
                else:
                    lst.append(None)
        return lst


class ScheduleData(models.Model):
    schedule = models.ForeignKey(Schedule,on_delete=models.CASCADE)
    week = models.IntegerField(default=0)
    start = models.CharField(max_length=5)
    end = models.CharField(max_length=5)

    def getStartInt(self):
        match = re.match(r"(\d+):(\d+)",self.start)
        return int(match.group(1)),int(match.group(2))

    def getEndInt(self):
        match = re.match(r"(\d+):(\d+)",self.end)
        return int(match.group(1)),int(match.group(2))



class Question(models.Model):
    task = models.ForeignKey(Tasks, on_delete = models.CASCADE)
    title = models.CharField(max_length = 32)
    fromSt =  models.ForeignKey(Students,on_delete=models.CASCADE)
    toTe = models.ForeignKey(Teachers,on_delete=models.CASCADE)
    finalup = models.DateTimeField(default=timezone.now)

    #AppoTimeを追加:days(何日後),何時(h),何分(m)
    def addAppo(self,days,h,m):
        now = timezone.now
        if(days > 0):
            now = now + datetime.timedelta(days = days)
        appo = AppoTime.objects.create(question = self,day = now,time = "{:0>2}:{:0>2}".format(h,m))
        appo.save()
        self.finalup = timezone.now
    
    def deleteAppoAll(self):
        if(AppoTime.objects.filter(question = self).exists()):
            appos = AppoTime.objects.filter(question = self)
            for appo in appos:
                appo.delete()


    def addAccept(self,appo):
        ac = Accept.objects.create(question = self,day = appo.day,time = appo.time)
        ac.save()
        self.deleteAppoAll()
        self.finalup = timezone.now
        
    #コメントの追加|生徒用    
    def addCommentSt(self,comment):
        comment = Comment.objects.create(question = self,comment = comment,isStudent = True)
        comment.save()
        self.finalup = timezone.now

    #コメントの追加|教師用
    def addCommentT(self,comment):
        comment = Comment.objects.create(question = self,comment = comment,isStudent = False)
        comment.save()
        self.finalup = timezone.now

    def getAppo(self):
        if(AppoTime.objects.filter(question = self).exists()):
            return AppoTime.objects.filter(question = self)
        else:
            return None

    def getAccept(self):
        if(Accept.objects.filter(question = self).exists()):
            return Accept.objects.filter(question = self)
        else:
            return None

    def getComment(self):
        if(Comment.objects.filter(question = self).exists()):
            return Comment.objects.filter(question = self)
        else:
            return None

    def gatAll(self):
        return self.getAppo(),self.getAccept(),self.getComment
        

class AppoTime(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    day = models.DateField(default=timezone.now) 
    time = models.CharField(max_length=5)

class Accept(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    day = models.DateField(default=timezone.now) 
    time = models.CharField(max_length=5)

class Comment(models.Model): 
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    comment = models.TextField()
    isStudent = models.BooleanField(default=False)
