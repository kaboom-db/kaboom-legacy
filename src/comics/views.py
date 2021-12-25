from .models import Character, Issue, Comic, Publisher, Staff, StaffPositions
from rest_framework import viewsets
from .serializers import IssueSerializer, PublisherSerializer, CharacterSerializer, SeriesSerializer, StaffPositionsSerializer, StaffSerializer
from django.db.models import Q
from django_filters import rest_framework as filters
from .comics_filters import IssuesFilter, PublishersFilters, StaffFilter, SeriesFilter, StaffPositionsFilter
from kaboom.utils import STATUS_OPTIONS
from rest_framework.response import Response

class PublisherView(viewsets.ReadOnlyModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PublishersFilters

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
    queryset = Comic.objects.all()
    serializer_class = SeriesSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SeriesFilter

class StaffPositionsView(viewsets.ReadOnlyModelViewSet):
    queryset = StaffPositions.objects.all()
    serializer_class = StaffPositionsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StaffPositionsFilter