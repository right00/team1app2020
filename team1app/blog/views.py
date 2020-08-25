from django.shortcuts import render
import requests

from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import SuspiciousOperation
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.contrib.auth.decorators import login_required





import django_filters
from rest_framework import viewsets, filters
from .models import User, Entry
from .serializer import UserSerializer, EntrySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    filter_fields = ('author', 'status')

@login_required
def home(request):
    return render(request, 'home.html')

def top(request):
    return render(request, 'top.html')

def Atask(request):
    return render(request, 'A_task.html')

def Bpurpose(request):
    return render(request, 'B_purpose.html')

def Creserve(request):
    return render(request, 'C_reserve.html')

def Dtag(request):
    return render(request, 'D_tag.html')

def Erec(request):
    return render(request, 'E_rec.html')
