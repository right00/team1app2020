from django.shortcuts import render,redirect
from blog.web_views_private import check
from blog.models import * 
from teachers.tools import * 
from django.utils import timezone
import datetime



# Create your views here.
def home(request):
    _,num = check(request)
    if num == 1:
        return render(request,'teachers/home.html')
    else:
        return redirect('home')

def edit_class(request):
    Me,num = check(request)
    if num != 1:
        return redirect('home')
    if request.method != 'POST':
        if (Me.classes_set.all()):
            classes=Me.classes_set.all()
            data = {"classes":classes,"all":False}
            return render(request,'teachers/class.html',data)
        return render(request,'teachers/class.html')
    elif request.POST["type"] == "my" :
        if (Me.classes_set.all()):
            classes=Me.classes_set.all()
            data = {"classes":classes,"all":False}
            return render(request,'teachers/class.html',data)
        return render(request,'teachers/class.html')
    elif request.POST["join"] !="":
        c = Classes.objects.filter(id = int(request.POST["join"]))
        if(c.filter(teachers=Me).exists()):
            result = "すでに参加済みのクラスです"
        else:   
            c[0].teachers.add(Me)
            c[0].save() 
            result = c[0].class_name+"に参加しました"
        base = Base.objects.get(id = Me.use_base)
        if (base.classes_set.all()):
            classes=base.classes_set.all()
            data = {"classes":classes,"all":True,"result":result}
            return render(request,'teachers/class.html',data)
    else:
        base = Base.objects.get(id = Me.use_base)
        if (base.classes_set.all()):
            classes=base.classes_set.all()
            data = {"classes":classes,"all":True}
            return render(request,'teachers/class.html',data)
    return render(request,'teachers/class.html')


def create_class(request):
    teacher,num = check(request)
    if num != 1:
        return redirect('home')
    elif request.method !="POST":
        return render(request,'teachers/CreateClass.html')
    else:
        base = Base.objects.get(id = teacher.use_base)
        if (base.classes_set.all()):
            classes=base.classes_set.all()
            for tarclass in classes:
                if(tarclass.class_name==request.POST["name"]):
                    result ="すでに存在するクラス名です。"
                    return render(request,'teachers/CreateClass.html',{"result":result})
        thisclass=Classes.objects.create(class_name=request.POST["name"],password = request.POST["password"],base=base)
        thisclass.teachers.add(teacher)
        thisclass.save()
        return redirect("/teacher/class/")

def class_content(request,classid):
    #教師以外はリダイレクト
    teacher,num = check(request)
    if num != 1:
        return redirect('home')
    #ユーザーが使用しているベースにクラスが属しているか確認
    have,thisclass=checkCL(teacher.use_base,classid)
    #クラスが属していた
    if have :
            #クラスに生徒がいる場合
            if (thisclass.students.all()!= None):
                sts = thisclass.students.all()
                data={"thisclass":thisclass,"sts":sts}
                return render(request,'teachers/Content.html',data)
            #クラスに生徒がいない場合
            else:
                data={"thisclass":thisclass}
                return render(request,'teachers/Content.html',data)
    #クラスが属していない
    else:
        return redirect("/teacher/class/")

def create_task(request,classid):
    #教師以外はリダイレクト
    teacher,num = check(request)
    if num != 1:
        return redirect('home')
    #ユーザーが使用しているベースにクラスが属しているか確認
    have,thisclass=checkCL(teacher.use_base,classid)
    #クラスが属していた
    if have :
        #メソッドがPOSTでなければタスク作成ページに移動    
        if request.method != "POST":
            return render(request,'teachers/TaskCreate.html')
        else:
            task=Tasks.objects.create(name=request.POST["name"],contents=request.POST["content"],tarclass=thisclass)
            task.auther.add(teacher)
            task.save()
            return redirect("/teacher/class/"+str(classid)+"/")
    else:
        return redirect("/teacher/class/")



def TasksList(request,classid):
    #教師以外はリダイレクト
    teacher,num = check(request)
    if num != 1:
        return redirect('home')
    #ユーザーが使用しているベースにクラスが属しているか確認
    if(not Classes.objects.get(id=classid).teachers.filter(id=teacher.id).exists()):
        return redirect("/teacher/class/")
    have,thisclass=checkCL(teacher.use_base,classid)
    #クラスが属していた
    if have :
        #メソッドがPOSTでなければタスク作成ページに移動    
        if(thisclass.tasks_set.all().filter(auther = teacher).exists()):
            tasks=thisclass.tasks_set.all().filter(auther = teacher)
            data = {"tasks":tasks}
            return render(request,'teachers/TaskList.html',data)
        else:
            return render(request,'teachers/TaskList.html')
    else:
        return redirect("/teacher/class/")

def taskContent(request,classid,taskid):
    teacher,num = check(request)
    if num != 1:
        return redirect('home')
    #ユーザーが使用しているベースにクラスが属しているか確認
    if(not Classes.objects.get(id=classid).teachers.filter(id=teacher.id).exists()):
        return redirect("/teacher/class/")
    have,thisclass=checkCL(teacher.use_base,classid)
    #クラスが属していた
    if have :
        #メソッドがPOSTでなければタスク作成ページに移動
        if request.method == "POST":
            if request.POST["type"] == "students":
                if request.POST.getlist("students"):
                    studentsid=request.POST.getlist("students")
                    thistask = Tasks.objects.get(id = taskid)
                    day=int(request.POST["days"])
                    days=[datetime.timedelta(days=1),datetime.timedelta(days=2),datetime.timedelta(days=3),datetime.timedelta(days=4),datetime.timedelta(days=5),datetime.timedelta(days=6),datetime.timedelta(weeks=1),datetime.timedelta(weeks=2),datetime.timedelta(weeks=4)]
                    for studentid in studentsid :
                        student = Students.objects.get(id=studentid)
                        homework=StudentTasks.objects.create(person=student,limit=timezone.now()+days[day])
                        homework.task.add(thistask)
                        homework.save()
                    return redirect("/teacher/class/")
        if(thisclass.tasks_set.all().filter(auther = teacher).exists()):
            tasks=thisclass.tasks_set.all().filter(auther = teacher)
            for task in tasks:
                if(task.id==taskid):
                    sts = thisclass.students.all()
                    data={"task":task,"students":sts}
                    return render(request,'teachers/TaskContent.html',data)
        else:
            return redirect("/teacher/class/")
    else:
        return redirect("/teacher/class/")



        
    
    



