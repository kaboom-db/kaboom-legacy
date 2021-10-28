from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Issue, Series

# Create your views here.
def index(request):
    return HttpResponse("Hello, you're visiting <strong>comics</strong>.")

def series_detail(request, series_id):
    series = get_object_or_404(Series, pk=series_id)
    return render(request, 'comics/series_detail.html', {'series': series})

def issue_detail(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    return render(request, 'comics/issue_detail.html', {'issue': issue})
    