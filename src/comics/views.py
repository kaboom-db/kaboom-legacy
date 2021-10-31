from django.db import models
from django.db.models import query
from django.http import HttpResponse, Http404
from .models import Character, Issue, Series, Publisher, Staff
from rest_framework import viewsets
from .serializers import PublisherSerializer, CharacterSerializer, StaffSerializer
from rest_framework_api_key.permissions import HasAPIKey
from django.db.models import Q

class PublisherView(viewsets.ReadOnlyModelViewSet):
    # Specify the serializer
    serializer_class = PublisherSerializer
    
    # Return the objects. If there is a filter query, it will match against that
    def get_queryset(self):
        queryset = Publisher.objects.all()
        query = self.request.query_params.get('query')
        if query:
            queryset = Publisher.objects.filter(name__contains=query)
        return queryset

class CharacterView(viewsets.ReadOnlyModelViewSet):
    serializer_class = CharacterSerializer

    def get_queryset(self):
        queryset = Character.objects.all()
        query = self.request.query_params.get('query')
        if query:
            queryset = Character.objects.filter(Q(name__contains=query) | Q(alias__contains=query))
        return queryset

class StaffView(viewsets.ReadOnlyModelViewSet):
    serializer_class = StaffSerializer

    def get_queryset(self):
        queryset = Staff.objects.all()
        position = self.request.query_params.get('position')
        query = self.request.query_params.get('query')
        if not position:
            position = 'all'
        
        if query and position != 'all':
            queryset = Staff.objects.filter(name__contains=query, position__contains=position)
        elif query and position == 'all':
            queryset = Staff.objects.filter(name__contains=query)

        return queryset
