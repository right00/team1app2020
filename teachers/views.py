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
        return redirect('teacher:teclass')
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
                data={"thisclass":thisclass,"sts":sts,"tags":tagsstate(thisclass,teacher)}
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
            return redirect("/teacher/class/"+str(classid)+"/task/"+str(task.id)+"/")
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
            if request.POST["type"] == "change":
                if(thisclass.tasks_set.all().filter(auther = teacher).exists()):
                    tasks=thisclass.tasks_set.all().filter(auther = teacher)
                    for task in tasks:
                        if(task.id==taskid):
                            task.name=request.POST["name"]
                            task.contents=request.POST["content"]
                            task.save()

            if request.POST["type"] == "addtags":
                tasks=thisclass.tasks_set.all().filter(auther = teacher)
                for task in tasks:
                    if(task.id==taskid):
                        if(task.tag.all().exists()):
                            nowtags = task.tag.all()
                            for tagid in request.POST.getlist("tags"):
                                if(nowtags.filter(id=int(tagid)).exists()):
                                    alert = "aleady exists"
                                    print(alert)
                                else:
                                    task.tag.add(Tags.objects.get(id = int(tagid)))
                                    task.save()
                        else:
                            for tagid in request.POST.getlist("tags"):
                                task.tag.add(Tags.objects.get(id = int(tagid)))
                                task.save()
            if request.POST["type"] == "delete":
                tasks=thisclass.tasks_set.all().filter(auther = teacher)
                for task in tasks:
                    if(task.id==taskid):
                        tagids=request.POST.getlist("tags")
                        for tagid in tagids :
                            tag = Tags.objects.get(id = int(tagid))
                            task.tag.remove(tag)
                        task.save()
        if(thisclass.tasks_set.all().filter(auther = teacher).exists()):
            tasks=thisclass.tasks_set.all().filter(auther = teacher)
            for task in tasks:
                if(task.id==taskid):
                    sts = thisclass.students.all()
                    thistags = None
                    tags = None
                    if (task.tag.all().exists()):
                        thistags = task.tag.all()
                    if(Tags.objects.filter(tarclass = thisclass).exists()):
                        tags = Tags.objects.filter(tarclass = thisclass)
                        data = {"tags":tags}
                    data={"task":task,"students":sts,"tags":tags,"thistags":thistags}
                    return render(request,'teachers/TaskContent.html',data)
        else:
            return redirect("/teacher/class/")
    else:
        return redirect("/teacher/class/")

def edit_tags(request,classid):
    teacher,num = check(request)
    if num != 1:
        return redirect('home')
    have,thisclass=checkCL(teacher.use_base,classid)
    if have :   
        if request.method != "POST":
            data = {}
            if(Tags.objects.filter(tarclass = thisclass).exists()):
                tags = Tags.objects.filter(tarclass = thisclass)
                data = {"tags":tags}
            return render(request,'teachers/tagsEdit.html',data)
        else:
            if request.method == "POST":
                alert = None
                tags = None
                if request.POST["type"] == "delete":
                    tagids=request.POST.getlist("tags")
                    for tagid in tagids :
                        tag = Tags.objects.get(id = int(tagid))
                        tag.delete()
                if request.POST["type"] == "add":
                    if(Tags.objects.filter(tarclass = thisclass,tag = request.POST["name"]).exists()):
                        alert = "aleady exists"
                    else:
                        tag = Tags.objects.create(tag=request.POST["name"],tarclass = thisclass)
                        tag.save()

                if(Tags.objects.filter(tarclass = thisclass).exists()):
                    tags = Tags.objects.filter(tarclass = thisclass)
                    data = {"tags":tags}

                data = {"tags":tags,"alert":alert}
                return render(request,'teachers/tagsEdit.html',data)
    else:
        return redirect("/teacher/class/")

def studentContents(request,classid,studentid):
    teacher,num = check(request)
    if num != 1:
        return redirect('home')
    have,thisclass=checkCL(teacher.use_base,classid)
    
    if not have :
        print(0)
        return redirect("/teacher/class/")
    
    cl,st = checkStudent(classid,studentid)
    
    if(cl == None):
        print(1)
        return redirect("/teacher/class/")

    data = {"Homeworks":st.getHomeworkT(teacher),"st":st}
    return render(request,'teachers/studentContents.html',data)

def schedule(request):
    teacher,num = check(request)
    if num != 1:
        return redirect('home') 
    if(not Schedule.objects.filter(person = teacher).exists()):
        sd = Schedule.objects.create(person = teacher)
        sd.save()
        data = {"hs":range(24),"ms":range(60)}
        return render(request,"teachers/schedule.html",data)
    else:
        sd = Schedule.objects.get(person = teacher)
        if(request.method == "POST"):
            sd.add(int(request.POST["week"]),int(request.POST["sh"]),int(request.POST["sm"]),int(request.POST["eh"]),int(request.POST["em"]))
        data = {"schedules":sd.getScheduleData(),"hs":range(24),"ms":range(60)}
    return render(request,"teachers/schedule.html",data)


def questions(request):
    teacher,num = check(request)
    if num != 1:
        return redirect('home') 
    q = teacher.getQuestions()
    data = {"questions":q}
    return render(request,"teachers/questions.html",data)

def question(request,id):
    teacher,num = check(request)
    if num != 1:
        return redirect('home') 
    if Question.objects.filter(id = id,toTe = teacher).exists():
        q = Question.objects.get(id=id)
        if request.method == "POST":
            q.addCommentT(request.POST["comment"])
        data = {"q":q,"Accept":q.getAccept(),"Appo":q.getAppo(),"Comment":q.getComment(),"student":q.fromSt,"teacher":q.toTe}
        return render(request,"teachers/questionContent.html",data)
    else:
        return redirect('home') 




    

    
    
    
    
    
    



        
    




    



        
    
    



