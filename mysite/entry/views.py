from django.shortcuts import render
from django.utils import timezone
from .models import entry
from django.http import HttpResponse
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.conf.urls import include
from django.conf.urls import url
from django.http import HttpRequest, HttpResponseRedirect as redirect


# Create your views here.

def home(request):
    return render(request, 'index.html')

'''
def search(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            exact_entry = entry.objects.filter(bhutia__iexact=q)
            entrys = entry.objects.filter(bhutia__icontains=q)

            #run comparisons

            return render(request,  'entry/entry_list.html', {'entrys': entrys, 'query': exact_entry})
        return render(request, 'entry/entry_list.html', {'error': error})
'''

def search(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']

        if not q:
            error = True
        else:
            if request.path == "/entry/bhutia_english/":
                exact_entry = entry.objects.filter(bhutia__iexact=q)
                entrys = entry.objects.filter(bhutia__icontains=q)
                return render(request, 'entry/entry_list.html', {'entrys': entrys, 'query': exact_entry})

            if request.path == "/entry/english_bhutia/":
                exact_entry = entry.objects.filter(english__iexact=q)
                entrys = entry.objects.filter(english__icontains=q)
                return render(request, 'entry/entry_list.html', {'entrys': entrys, 'query': exact_entry})

            if request.path == "/entry/tibetan_bhutia/":
                exact_entry = entry.objects.filter(tibetan__iexact=q)
                entrys = entry.objects.filter(tibetan__icontains=q)
                return render(request, 'entry/entry_list.html', {'entrys': entrys, 'query': exact_entry})
        return render(request, 'entry/entry_list.html', {'error': error})

def autocorrect(q):
    
    return