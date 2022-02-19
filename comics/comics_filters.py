from django_filters import rest_framework as filters
from comics.models import Format, Issue, Publisher, Staff, Comic, StaffPositions

class StaffFilter(filters.FilterSet):
    query = filters.filters.CharFilter(field_name='name', lookup_expr='icontains')
    position = filters.filters.CharFilter(field_name='position', lookup_expr='position__iexact')

    class Meta:
        model = Staff
        fields = ['name', 'position']

class StaffPositionsFilter(filters.FilterSet):
    position = filters.filters.CharFilter(field_name='position', lookup_expr='icontains')

    class Meta:
        model = StaffPositions
        fields = ['position']

class SeriesFilter(filters.FilterSet):
    query = filters.filters.CharFilter(field_name='series_name', lookup_expr='icontains')
    status = filters.filters.CharFilter(field_name='status', lookup_expr='icontains')
    year = filters.filters.NumberFilter(field_name='year_started')
    publisher = filters.filters.NumberFilter(field_name='publisher')

    class Meta:
        model = Comic
        fields = ['series_name', 'year_started', 'status', 'publisher']

class IssuesFilter(filters.FilterSet):
    series = filters.filters.NumberFilter(field_name='series')
    issue_number_absolute = filters.filters.NumberFilter(field_name='issue_number_absolute')
    issue_name = filters.filters.CharFilter(field_name='issue_name', lookup_expr='icontains')

    class Meta:
        model = Issue
        fields = ['series', 'issue_number_absolute', 'issue_name']

class PublishersFilters(filters.FilterSet):
    query = filters.filters.CharFilter(field_name='name', lookup_expr='icontains')
    
    class Meta:
        model = Publisher
        fields = ['name']

class FormatFilter(filters.FilterSet):
    name= filters.filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Format
        fields = ['name']