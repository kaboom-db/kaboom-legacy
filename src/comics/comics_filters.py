from django_filters import rest_framework as filters
from comics.models import Issue, Publisher, Staff, Series, StaffPositions

class StaffFilter(filters.FilterSet):
    query = filters.filters.CharFilter(field_name='name', lookup_expr='icontains')
    position = filters.filters.NumberFilter(field_name='position')

    class Meta:
        model = Staff
        fields = ['name', 'position']

class StaffPositionsFilter(filters.FilterSet):
    position = filters.filters.NumberFilter(field_name='position')

    class Meta:
        model = StaffPositions
        fields = ['position']

class SeriesFilter(filters.FilterSet):
    query = filters.filters.CharFilter(field_name='series_name', lookup_expr='icontains')
    status = filters.filters.CharFilter(field_name='status', lookup_expr='icontains')
    year = filters.filters.NumberFilter(field_name='year_started')

    class Meta:
        model = Series
        fields = ['series_name', 'year_started', 'status']

class IssuesFilter(filters.FilterSet):
    series = filters.filters.NumberFilter(field_name='series')

    class Meta:
        model = Issue
        fields = ['series']

class PublishersFilters(filters.FilterSet):
    query = filters.filters.CharFilter(field_name='name', lookup_expr='icontains')
    
    class Meta:
        model = Publisher
        fields = ['name']