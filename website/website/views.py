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
        # data = {
        #     'Fields': [{'title': 'Computer science', 'url': 'https://en.wikipedia.org/wiki/Computer_science'}],
        #     'Alma mater': [{'title': 'Princeton University', 'url': 'https://en.wikipedia.org/wiki/Princeton_University'}, {'title': 'California Institute of Technology', 'url': 'https://en.wikipedia.org/wiki/California_Institute_of_Technology'}],
        #     'wiki url': 'https://en.wikipedia.org/wiki/John_McCarthy_(computer_scientist)',
        #     'Known for': [{'title': 'Artificial intelligence', 'url': 'https://en.wikipedia.org/wiki/Artificial_intelligence'}, {'title': 'Lisp', 'url': 'https://en.wikipedia.org/wiki/Lisp_(programming_language)'}, {'title': 'circumscription', 'url': 'https://en.wikipedia.org/wiki/Circumscription_(logic)'}, {'title': 'situation calculus', 'url': 'https://en.wikipedia.org/wiki/Situation_calculus'}],
        #     'Doctoral advisor': [{'title': 'Solomon Lefschetz', 'url': 'https://en.wikipedia.org/wiki/Solomon_Lefschetz'}],
        #     'Institutions': [{'title': 'Stanford University', 'url': 'https://en.wikipedia.org/wiki/Stanford_University'}, {'title': 'Massachusetts Institute of Technology', 'url': 'https://en.wikipedia.org/wiki/Massachusetts_Institute_of_Technology'}, {'title': 'Dartmouth College', 'url': 'https://en.wikipedia.org/wiki/Dartmouth_College'}, {'title': 'Princeton University', 'url': 'https://en.wikipedia.org/wiki/Princeton_University'}],
        #     'Born': {'day': '1927-09-04', 'place': 'Boston, Massachusetts, U.S.'},
        #     'Awards': [{'title': 'Turing Award', 'year': '1971'}, {'title': 'Computer Pioneer Award', 'year': '1985'}, {'title': 'IJCAI Award for Research Excellence', 'year': '1985'}, {'title': 'Kyoto Prize', 'year': '1988'}, {'title': 'National Medal of Science', 'year': '1990'}],
        #     'name': 'John McCarthy',
        #     'Doctoral students': [{'title': 'Ruzena Bajcsy', 'url': 'https://en.wikipedia.org/wiki/Ruzena_Bajcsy'}, {'title': 'Ramanathan V. Guha', 'url': 'https://en.wikipedia.org/wiki/Ramanathan_V._Guha'}, {'title': 'Barbara Liskov', 'url': 'https://en.wikipedia.org/wiki/Barbara_Liskov'}, {'title': 'Raj Reddy', 'url': 'https://en.wikipedia.org/wiki/Raj_Reddy'}],
        #     'Died': {'day': '(2011-10-24)', 'place': 'Stanford, California, U.S.'}
        # }
        data = prepare_context(data)
        return render(request, 'people.html', data)
    else:
        return index(request)

def prepare_context(data):
    res = {}
    for k in data:
        res[k.replace(' ', '_')] = data[k]
    return res