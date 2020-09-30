from django.shortcuts import render,redirect
from blog.web_views_private import check

# Create your views here.
def home(request):
    _,num = check(request)
    if num == 2:
        return render(request,'students/home.html')
    else:
        return redirect('home')


def task(request):
    """task画面"""
    return render(request, 'students/task.html')

def propose(request):
    """propose画面"""
    return render(request, 'students/propose.html')

def reserve(request):
    """reserve画面"""
    return render(request, 'students/reserve.html')

def tag(request):
    """tag画面"""
    return render(request, 'students/tag.html')

