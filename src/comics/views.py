from django.http import HttpResponse, Http404
from .models import Character, Issue, Series, Publisher, Staff
from rest_framework import viewsets
from .serializers import PublisherSerializer
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework import generics

# Create your views here.
def index(request):
    return HttpResponse("hello")

class PublisherView(viewsets.ModelViewSet):
    # Specify the serializer
    serializer_class = PublisherSerializer
    
    # Return the objects. If there is a filter query, it will match against that
    def get_queryset(self):
        queryset = Publisher.objects.all()
        query = self.request.query_params.get('query')
        if query:
            queryset = Publisher.objects.filter(name__contains=query)
        return queryset