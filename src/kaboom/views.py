from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

def index(request):
    return HttpResponse("<h1>Welcome to KABOOM</h1><p><a href=\"{% url 'comics:index' %}\">Comics</a></p>")