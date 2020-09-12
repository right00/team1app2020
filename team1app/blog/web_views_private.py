from django.shortcuts import render

def home(request):
    return render(request,'blog/private/home.html')