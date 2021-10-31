from .models import Character, Issue, Series, Publisher, Staff
from rest_framework import viewsets
from .serializers import IssueSerializer, PublisherSerializer, CharacterSerializer, SeriesSerializer, StaffSerializer
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
        elif not query and position != 'all':
            queryset = Staff.objects.filter(position__contains=position)
        elif not query and position == 'all':
            queryset = Staff.objects.all()

        return queryset

class IssueView(viewsets.ReadOnlyModelViewSet):
    serializer_class = IssueSerializer

    def get_queryset(self):
        queryset = Issue.objects.all()
        series_id = self.request.query_params.get('series_id')
        if series_id:
            queryset = Issue.objects.filter(series__id=series_id)
        return queryset

# class SeriesView(viewsets.ReadOnlyModelViewSet):
#     serializer_class = SeriesSerializer
#     
#     def get_queryset(self):
#         queryset = Series.objects.all()
#         # series_name, year_started, status
#         year = self.request.query_params.get('year')
#         status = self.request.query_params.get('status')
#         query = self.request.query_params.get('query')
#         
#         if not status:
#             status = 'all'
#         
#         if query and status != 'all' and year:
#             # We have all of them
#             queryset = Series.objects.filter(series_name__contains=query, status__contains=status, year_started=year)
#         elif query and status != 'all' and not year:
#             # No year
#             queryset = Series.objects.filter(series_name__contains=query, status__contains=status)
#         elif query and status == 'all' and not year:
#             # Only query
#             queryset = Series.objects.filter(series_name__contains=query)
#         elif not query and status == 'all' and not year:
#             # None
#             queryset = Series.objects.all()
#         elif not query and status != 'all' and not year:
#             # Only status
#             queryset = Series.objects.filter(status__contains=status)
#         elif not query 
#             
#         
#         return queryset