from django.shortcuts import render
from django.utils import timezone
from .models import entry
from django.http import HttpResponse


# Create your views here.

def home(request):
    return render(request, 'entry/index.html')

def entry_list(request):
    entrys = entry.objects.all()
    return render(request, 'entry/entry_list.html', {"entrys" : entrys})

   