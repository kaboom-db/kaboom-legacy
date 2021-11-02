from django_filters import rest_framework as filters
from cartoons.models import Cartoon

class CartoonFilter(filters.FilterSet):
    query = filters.filters.CharFilter(field_name='name', lookup_expr='contains')
    genre = filters.filters.CharFilter(field_name='genres', lookup_expr='contains')
    network = filters.filters.CharFilter(field_name='network', lookup_expr='contains')

    class Meta:
        model = Cartoon
        fields = ['name', 'genres', 'network']

# class StaffFilter(filters.FilterSet):
#     query = filters.filters.CharFilter(field_name='name', lookup_expr='contains')
#     position = filters.filters.CharFilter(field_name='position', lookup_expr='contains')
# 
#     class Meta:
#         model = Staff
#         fields = ['name', 'position']
# 
# class SeriesFilter(filters.FilterSet):
#     query = filters.filters.CharFilter(field_name='series_name', lookup_expr='contains')
#     status = filters.filters.CharFilter(field_name='status', lookup_expr='contains')
#     year = filters.filters.NumberFilter(field_name='year_started')
# 
#     class Meta:
#         model = Series
#         fields = ['series_name', 'year_started', 'status']