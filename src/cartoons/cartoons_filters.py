from django_filters import rest_framework as filters
from cartoons.models import Cartoon

class CartoonFilter(filters.FilterSet):
    query = filters.filters.CharFilter(field_name='name', lookup_expr='contains')
    genre = filters.filters.CharFilter(field_name='genres', lookup_expr='contains')
    network = filters.filters.CharFilter(field_name='network', lookup_expr='contains')

    class Meta:
        model = Cartoon
        fields = ['name', 'genres', 'network']