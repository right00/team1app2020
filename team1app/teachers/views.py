from django.shortcuts import render,redirect
from blog.web_views_private import check
from blog.models import * 

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
