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
    if request.method != 'POST':
        if (student.classes_set.all()):
            classes = student.classes_set.all()
            data = {"classes":classes, "all":False}
            return render(request, 'task.html', data)
        return render(request, 'task.html')
    elif request.POST["type"] == "my" :
        if (student.classes_set.all()):
            classes = student.classes_set.all()
            data = {"classes":classes, "all":False}
            return render(request,'task.html', data)
        return render(request, 'task.html')
    else:
        return redirect("home")
    if request.method =='POST':
        tasks = Tasks(name = request.POST["name"], contents = request.POST['contents'], tarclass = thisclass)
        tasks.save()
    context = {'tasks':tasks}
    return render(request, 'task.html', context)

def propose(request):
    """propose画面"""
    _,num = check(request)
    if num == 2:
        return render(request, 'propose.html')
    else:
        return redirect('home')

def reserve(request):
    _,num = check(request)
    if num == 2:
        return render(request, 'reserve.html')
    else:
        return redirect('home')

#def reserve(request, id):
 #   """reserve画面"""
  #  student, num = check(request)
   # if num != 2:
    #    return redirect('home') 
    ##if Question.objects.filter(id = id, fromSt = student).exists():
      #  q = Question.objects.get(id=id)
       # if request.method == "POST":
        #    q.addCommentSt(request.POST["comment"])
        #data = {"q":q,"Accept":q.addAppo(),"Appo":q.addAppo(), "Comment":q.getComment(),"student":q.fromSt,"teacher":q.toTe}
        #return render(request,"students/reserve.html", data)
    #else:
     #   return redirect('home') 

def tag(request):
    """tag画面"""
    _,num = check(request)
    if num == 2:
        return render(request, 'tag.html')
    else:
        return redirect('home')


def chat(request):
    student,num = check(request)
    if num != 2:
        return redirect('home') 
    q = student.getQuestions()
    data = {"questions": q }
    return render(request,'chat.html', data)

    #messages = Message.objects.filter(room_name = room_name).order_by('-created_at')
    #messages = Question.objects.filter(room_name = Teachers).order_by('-created_at')

  #  message = Question.objects.filter(id = id, toTe = teacher).
   # room = Question

#auther toTEに直接つっこむ


#getQuestion

def room(request, id):
    student, num = check(request)
    if num != 2:
        return redirect('home') 
    if Question.objects.filter(id = id, flomSt = student).exists():
        q = Question.objects.get(id = id)
        if request.method == "POST":
            q.addCommentSt(request.POST["comment"])
            q.addAppo(request.POST["appo"])
        data = {"q":q,"Accept":q.getAccept(),"Appo":q.getAppo() ,"Comment":q.getComment(),"student":q.fromSt,"teacher":q.toTe}
        return render(request,'room.html', data)
    else:
        return redirect('home') 
