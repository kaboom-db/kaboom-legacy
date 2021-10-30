from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Character, Issue, Series, Publisher, Staff

# Create your views here.
def index(request):
    # Get all series released in 2021
    series_list = Series.objects.filter(year_started=2021)
    return render(request, 'comics/comics.html', {'series_list': series_list})

def series_detail(request, series_id):
    series = get_object_or_404(Series, pk=series_id)
    return render(request, 'comics/series_detail.html', {'series': series})

def issue_detail(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    return render(request, 'comics/issue_detail.html', {'issue': issue})

def publisher_detail(request, publisher_id):
    publisher = get_object_or_404(Publisher, pk=publisher_id)
    return render(request, 'comics/publisher_detail.html', {'publisher': publisher})

def staff_detail(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    return render(request, 'comics/staff_detail.html', {'staff': staff})

def character_detail(request, character_id):
    character = get_object_or_404(Character, pk=character_id)
    return render(request, 'comics/character_detail.html', {'character': character})
