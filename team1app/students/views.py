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
    return render(request, 'students/home/task.html')

def propose(request):
    """propose画面"""
    return render(request, 'students/propose.html')

def reserve(request):
    """reserve画面"""
    return render(request, 'students/reserve.html')

def tag(request):
    """tag画面"""
    return render(request, 'students/tag.html')

