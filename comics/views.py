from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Series

# Create your views here.
def index(request):
    return HttpResponse("Hello, you're visiting <strong>comics</strong>.")

def series_detail(request, series_id):
    series = get_object_or_404(Series, pk=series_id)
    return render(request, 'comics/series_detail.html', {'series': series})
    