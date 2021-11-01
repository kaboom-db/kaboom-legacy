from django_filters import rest_framework as filters
from comics.models import Staff, Series

class StaffFilter(filters.FilterSet):
    query = filters.filters.CharFilter(field_name='name', lookup_expr='contains')
    position = filters.filters.CharFilter(field_name='position', lookup_expr='contains')

    class Meta:
        model = Staff
        fields = ['name', 'position', 'image', 'id']

class SeriesFilter(filters.FilterSet):
    query = filters.filters.CharFilter(field_name='series_name', lookup_expr='contains')
    status = filters.filters.CharFilter(field_name='status', lookup_expr='contains')
    year = filters.filters.NumberFilter(field_name='year_started')

    class Meta:
        model = Series
        fields = ['series_name', 'publisher', 'description', 'year_started', 'status', 'id', 'image_small', 'image_medium', 'image_large']