from django.shortcuts import render,redirect
from blog.web_views_private import check
from blog.models import * 

# Create your views here.
def home(request):
    _,num = check(request)
    if num == 2:
        return render(request,'home.html')
    else:
        return redirect('home')


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

