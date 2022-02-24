from django_filters import rest_framework as filters
from .models import Thought, Comment

class ThoughtFilter(filters.FilterSet):
    user = filters.filters.CharFilter(field_name='user', lookup_expr='iexact')
    thought_type = filters.filters.CharFilter(field_name='thought_type', lookup_expr='iexact')
    related_object_id = filters.filters.NumberFilter(field_name='related_object_id')
    date_created = filters.filters.DateFromToRangeFilter(field_name='date_created')

    class Meta:
        model = Thought
        fields = '__all__'