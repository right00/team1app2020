from django.shortcuts import render

def home(request):
    return render(request,'blog/private/home.html')

def task(request):
    return render(request, 'blog/private/task.html')

def propose(request):
    return render(request, 'blog/private/propose.html')

def reserve(request):
    return render(request, 'blog/private/reserve.html')

def tag(request):
    return render(request, 'blog/private/tag.html')
