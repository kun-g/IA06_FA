from django.http import HttpResponse
from django.shortcuts import render

# from . import wikipedia
from .wikipedia import get_people

#data = get_people(wiki_ur)

def index(request):
    context = {}
    return render(request, 'index.html', context)

def wikipedia(request):
    if request.POST and request.POST['url']:
        return HttpResponse(get_people(request.POST['url']))
    else:
        return index(request)