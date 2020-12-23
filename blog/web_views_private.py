from django.shortcuts import render ,redirect
from blog.models import * 
from django.contrib.auth.decorators import login_required

def check(request):
    user = request.user
    if Teachers.objects.filter(person = user).count() > 0:
        if Teachers.objects.get(person = user).use_base ==None:
            try:
                me = Teachers.objects.get(person = user)
                bases = me.base_set.all()
                me.use_base = bases[0].id
                me.save()
            except:
                return Teachers.objects.get(person = user),1
        return Teachers.objects.get(person = user),1
    if Students.objects.filter(person = user).count() > 0:
        if Students.objects.get(person = user).use_base ==None:
            try:
                me = Students.objects.get(person = user)
                bases = me.base_set.all()
                me.use_base = bases[0].id
                me.save()
            except:
                return Students.objects.get(person = user),2
        return Students.objects.get(person = user),2
    else:
        return None,0

@login_required
def home(request):
    _,num = check(request)
    if num == 1:
        return redirect('tehome')
    if num == 2:
        return redirect('sthome')
    return render(request,'blog/private/home.html')

@login_required
def makegroup(request):
    p,num = check(request)
    if  num == 0:
        if request.method == 'POST':
            if not (request.POST["groupname"] != ""  and Base.objects.filter(base_name = request.POST["groupname"]).count() == 0) :
                poste = True
                error="すでに使用されているグループ名です。"
                content = {'poste':poste,'error':error}
                return render(request,'blog/private/makegroup.html',content)
            if request.POST["password"] ==  request.POST["password2"]:
                poste = True
                error="パスワード1とパスワード2は違う値にしてください。"
                content = {'poste':poste,'error':error}
                return render(request,'blog/private/makegroup.html',content)
            else:
                user = request.user
                base = Base.objects.create(base_name = request.POST["groupname"],password = request.POST["password"],password2=request.POST["password2"])
                teacher = Teachers.objects.create(name = request.POST["name"],person = user,use_base=base.id)
                teacher.save()
                base.administrator.add(user)
                base.teachers.add(teacher)
                base.save()
                return redirect("../home/")
        return render(request,'blog/private/makegroup.html')
    return redirect("../home/")

@login_required
def signincrassroom(request):
    p,num = check(request)
    if num != 0:
        return redirect('home')
    if request.method == 'POST':
        if Base.objects.filter(base_name = request.POST["groupname"]).count() == 0:
            poste = True
            error="存在しないグループ名です"
            content = {'poste':poste,'error':error}
            return render(request,'blog/private/join.html',content)
        
        elif request.POST["role"] == "teacher" :
            base = Base.objects.get(base_name = request.POST["groupname"])
            if base.password == request.POST["password"]:
                user = request.user
                teacher = Teachers.objects.create(name = request.POST["name"],person = user)
                teacher.save()
                base.teachers.add(teacher)
                base.save()
                return redirect('home')
            else:
                poste = True
                error="パスワードが間違っています"
                content = {'poste':poste,'error':error}
                return render(request,'blog/private/join.html',content)
        else: 
            base = Base.objects.get(base_name = request.POST["groupname"])
            if base.password2 == request.POST["password"]:
                user = request.user
                student = Students.objects.create(name = request.POST["name"],person = user)
                student.save()
                base.students.add(student)
                base.save()
                return redirect('home')
            else:
                poste = True
                error="パスワードが間違っています"
                content = {'poste':poste,'error':error}
                return render(request,'blog/private/join.html',content)

    return render(request,'blog/private/join.html')
