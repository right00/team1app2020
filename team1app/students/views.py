from django.shortcuts import render,redirect
from blog.web_views_private import check
from blog.models import * 
from students.tools import * 

# Create your views here.
def home(request):
    """studentのhome画面"""
    user_student,num = check(request)
    if num != 2:
        return redirect('home')
    if request.method != 'POST':
        if (user_student.classes_set.all()):
            classes = user_student.classes_set.all()
            data = {"classes":classes,"all":False}
            return render(request, 'home.html', data)
        return render(request, 'home.html')
    elif request.POST["type"] == "my" :
        if (user_student.classes_set.all()):
            classes = user_student.classes_set.all()
            data = {"classes":classes, "all":False}
            return render(request,'home.html', data)
        return render(request, 'home.html')
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
            data = {"classes":classes,"all":True,"result":result}
            return render(request,'home.html',data)
    else:
        base = Base.objects.get(id = user_student.use_base)
        if (base.classes_set.all()):
            classes=base.classes_set.all()
            data = {"classes":classes, "all":True}
            return render(request, 'home.html', data)
    return render(request, 'home.html')

def class_page(request,classid):
    """studentのclass_page画面"""
    #生徒以外はリダイレクト
    student,num = check(request)
    if num != 2:
        return redirect('home')
    #ユーザーが使用しているベースにクラスが属しているか確認
    have, thisclass = checkCL(student.use_base, classid)
    #クラスが属していた
    if have :
             # クラスに出された宿題を表示する
            if request.method =='POST':
                tasks = Tasks(name = request.POST["name"], contents = request.POST['contents'], tarclass = thisclass)
                tasks.save()
                context = {'tasks':tasks}
                return render(request, 'class_page.html', context)
            #クラスに生徒がいない場合
            else:
                data= { "thisclass" : thisclass }
                return render(request,'class_page.html',data)
    #クラスに属していない
    else:
        return redirect("/student/home/")


def task(request):
    """task画面"""
    _,num = check(request)
    if num == 2:
        return render(request,'task.html')
    else:
        return redirect('home')
  
def propose(request):
    """propose画面"""
    _,num = check(request)
    if num == 2:
        return render(request, 'propose.html')
    else:
        return redirect('home')

def reserve(request):
    """reserve画面"""
    _,num = check(request)
    if num == 2:
        return render(request, 'reserve.html')
    else:
        return redirect('home')

def tag(request):
    """tag画面"""
    _,num = check(request)
    if num == 2:
        return render(request, 'tag.html')
    else:
        return redirect('home')

