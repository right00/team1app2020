from django.shortcuts import render,redirect
from blog.web_views_private import check
from blog.models import * 
from students.tools import * 
from django.utils import timezone
import datetime

# Create your views here.
def home(request):
    """studentのhome画面"""
    user_student,num = check(request)
    data = {"html":"background-image:url(../../../static/img/math.png)"}
    if num != 2:
        return redirect('home')
    if request.method != 'POST':
        if (user_student.classes_set.all()):
            classes = user_student.classes_set.all()
            data = {"classes":classes,"all":False,"html":"background-image:url(../../../static/img/math.png)"}
            return render(request, 'home.html', data)
        return render(request, 'home.html',data)
    elif request.POST["type"] == "my" :
        if (user_student.classes_set.all()):
            classes = user_student.classes_set.all()
            data = {"classes":classes, "all":False, "html":"background-image:url../../../static/img/math.png)"}
            return render(request,'home.html', data)
        return render(request, 'home.html',data)
    elif request.POST["join"] !="":
        c = Classes.objects.filter(id = int(request.POST["join"]))
        if(c.filter(students = user_student).exists()):
            result = "すでに参加済みのクラスです"
        else:   
            c[0].students.add(user_student)
            c[0].save() 
            result = c[0].class_name + "に参加しました"
        base = Base.objects.get(id = user_student.use_base)
        if (base.classes_set.all()):
            classes=base.classes_set.all()
            data = {"classes":classes,"all":True,"result":result,"html":"background-image:url(../../../static/img/math.png)"}
            return render(request,'home.html',data)    
    else:
        base = Base.objects.get(id = user_student.use_base)
        if (base.classes_set.all()):
            classes=base.classes_set.all()
            data = {"classes":classes, "all":True}
            return render(request, 'home.html', data)
    return render(request, 'home.html',data)

def class_page(request,class_id):
    """studentのclass_page画面"""
    #生徒以外はリダイレクト
    student,num = check(request)
    if num != 2:
        return redirect('home')
    #ユーザーが使用しているベースにクラスが属しているか確認
    have, thisclass = checkCL(student.use_base, class_id)
    #クラスが属していた
    if have :
            #クラスに生徒がいる場合
            if (thisclass.students.all()!= None):
                if(student.studenttasks_set.all().exists()):
                    tasks=student.studenttasks_set.all()
                    tasks2=[]
                    for i in tasks:
                        task = gettask(i)
                        if(task.tarclass==thisclass):
                            data={"task":i,"name":task.name,"contents":task.contents}
                            tasks2.append(data)
                    context = {'tasks':tasks2}
                    return render(request, 'class_page.html', context)
                return render(request, 'class_page.html')
            #クラスに生徒がいない場合
            else:
                data= { "thisclass" : thisclass }
                return render(request,'class_page.html',data)
    #クラスに属していない
    else:
        return redirect("/student/home/")
    # クラスに出された宿題を表示する
    if request.method =='POST':
        tasks = Tasks(name = request.POST["name"], contents = request.POST['contents'], tarclass = thisclass)
        tasks.save()
    context = {'tasks':tasks}
    return render(request, 'class_page.html', context)

def task(request):
    """task画面"""
    student,num = check(request)
    if num != 2:
        return redirect('home')
    datas = student.getMyClassHomework()
    data  = {
        'datas' : datas
    }
    return render(request, 'task.html', data)

def propose(request):
    """propose画面"""
    _,num = check(request)
    if num == 2:
        return render(request, 'propose.html')
    else:
        return redirect('home')

def tag(request):
    """tag画面"""
    cnt = 0
    #生徒以外はリダイレクト
    student,num = check(request)
    if num != 2:
        return redirect('home')
    
    if request.method == "POST":
        finish1 = request.POST["userid1"]
        content = finish1.split(":")
        
        for i in range(int(len(content)/3)):
            if content[i] =="":
                break
            task=StudentTasks.objects.get(id = int(content[i * 3]))
            task.finish = True
            if(content[i * 3 + 2] == "true"):
                task.result = True
            task.save()
        
    if(student.studenttasks_set.all().exists()):
        tasks=student.studenttasks_set.all()
        classes = student.classes_set.all()
        tasks2=[]
        for i in tasks:
            task = gettask(i)
            if i.finish ==0:
                cnt +=1
            data={"task":i,"name":task.name,"contents":task.contents}
            tasks2.append(data)
        context = {'tasks':tasks2,'cnt':cnt,"classes":classes}
        return render(request, 'tag.html', context)
    else:
        classes = student.classes_set.all()
        context = {"classes":classes}
        return render(request, 'tag.html',context)
    

def chat(request):
    student,num = check(request)
    if num != 2:
        return redirect('home') 
    if request.method == 'POST':
        teacher = Teachers.objects.get( id = int(request.POST["select_teachers"]))
        task = Tasks.objects.get(id = int(request.POST["select_tasks"]))
        questions = Question.objects.create(title = request.POST['comment'], task = task, toTe = teacher, fromSt = student)
        print(questions)
        questions.save()
    q = student.getQuestions()
    data = {"questions": q }
    return render(request,'chat.html', data)

def chat_create(request):
    student, num = check(request)
    if num != 2:
        return redirect('home')   
    if request.method == 'POST':
        teacher = Teachers.objects.get( id = int(request.POST["select_teachers"]))
        task = Tasks.objects.get(id = int(request.POST["select_tasks"]))
        questions = Question.objects.create(title = request.POST['comment'], task = task, toTe = teacher, fromSt = student)
        print(questions)
        questions.save()
    questions = Question.objects.order_by('-finalup')   
    teacher_name = Teachers.objects.all()
    task_name = Tasks.objects.all()
    context = {
            "teacher" : teacher_name,
            "questions": questions,
            "tasks" : task_name
    }
    return render(request, 'chat_create.html', context)
   
def room(request, id):
    student, num = check(request)
    if num != 2:
        return redirect('home') 
    text = "コメントを入力"
    if request.method == "POST":
        if(request.POST["type"] == "comment"):
            Question.objects.get(id = id).addCommentSt(request.POST["comment"])
        else:
            text = request.POST["comment"]
    context = {
        'Comment' : Question.objects.get(id = id).getComment(),
        'one' :  Question.objects.get(id = id),
        'text': text,
    }
    return render(request, 'room.html', context)
