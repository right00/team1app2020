from django.shortcuts import render ,redirect
from blog.models import * 

def home(request):
    return render(request,'blog/private/home.html')

def makegroup(request):
    if request.method == 'POST':
        base = Base.objects.create(base_name = request.POST["groupname"],password = request.POST["password"])
        user = request.user
        base.administrator.add(user)
        base.save()
        return redirect("../home/")
    return render(request,'blog/private/makegroup.html')

def signincrassroom(request):
    return render(request,'blog/private/signcrassroom.html')
