from django.shortcuts import render
from django.utils import timezone
from .models import entry
from django.http import HttpResponse


# Create your views here.

def home(request):
    return render(request, 'index.html')

def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        entrys = entry.objects.filter(bhutia__icontains=q)
        if entrys:
            return render(request, 'entry/entry_list.html',
                          {'entrys': entrys, 'query': q})
        else:
            error = True
            return render(request, 'entry/entry_list.html', {'error': error})

    else:
        error = True
        return render(request, 'entry/entry_list.html', {'error': error})
#
#
# def search(request):
#     error = False
#     if 'q' in request.GET:
#         q = request.GET['q']
#         if not q:
#             error = True
#         else:
#             books = entry.objects.filter(bhutia__icontains=q)
#             return render(request, 'entry/entry_list.html', {'books': books, 'query': q})
#     return render(request, 'index.html', {'error': error})