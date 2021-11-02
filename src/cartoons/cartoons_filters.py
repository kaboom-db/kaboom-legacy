from django_filters import rest_framework as filters
from .models import Series

class SeriesFilter(filters.FilterSet):
    query = filters.filters.CharFilter(field_name='name', lookup_expr='contains')
    genre = filters.filters.CharFilter(field_name='genres')
    network = filters.filters.CharFilter(field_name='network')

    class Meta:
        model = Series
        fields = ['name', 'genres', 'network']