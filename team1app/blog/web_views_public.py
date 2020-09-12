from django.shortcuts import render

def top(request):
    return render(request,'blog/public/top.html')