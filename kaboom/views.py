from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def v1(request):
    return render(request, 'v1/v1.html')