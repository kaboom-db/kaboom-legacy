from .models import Character, Issue, Series, Publisher, Staff
from rest_framework import viewsets
from .serializers import IssueSerializer, PublisherSerializer, CharacterSerializer, SeriesSerializer, StaffSerializer
from rest_framework_api_key.permissions import HasAPIKey
from django.db.models import Q
from django_filters import rest_framework as filters
from .comics_filters import IssuesFilter, StaffFilter, SeriesFilter

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
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StaffFilter

class IssueView(viewsets.ReadOnlyModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IssuesFilter

class SeriesView(viewsets.ReadOnlyModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SeriesFilter