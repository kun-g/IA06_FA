from django.http import HttpResponse
from django.shortcuts import render

# from . import wikipedia
from .wikipedia import get_people, render_md

#data = get_people(wiki_ur)

def index(request):
    context = {}
    return render(request, 'index.html', context)

def wikipedia(request):
    if request.POST and request.POST['url']:
        data = get_people(request.POST['url'])
        print(data)
        return HttpResponse(render_md(data))
    else:
        return index(request)