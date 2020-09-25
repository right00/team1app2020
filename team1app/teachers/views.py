from django.shortcuts import render,redirect
from blog.web_views_private import check

# Create your views here.
def home(request):
    _,num = check(request)
    if num == 1:
        return render(request,'teachers/home.html')
    else:
        return redirect('home')