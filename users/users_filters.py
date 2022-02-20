from django_filters import rest_framework as filters
from users.models import Thought, UserData
from django.contrib.auth.models import User

class ThoughtFilter(filters.FilterSet):
    user = filters.filters.CharFilter(field_name='user', lookup_expr='username__iexact')
    thought_type = filters.filters.CharFilter(field_name='thought_type', lookup_expr='model__iexact')
    related_object_id = filters.filters.NumberFilter(field_name='related_object_id')
    date_created = filters.filters.DateFromToRangeFilter(field_name='date_created')

    class Meta:
        model = Thought
        fields = '__all__'

class UserFilter(filters.FilterSet):
    username = filters.filters.CharFilter(field_name='username', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['username']

class UserDataFilter(filters.FilterSet):
    username = filters.filters.CharFilter(field_name='user', lookup_expr='username__icontains')

    class Meta:
        model = UserData
        fields = ['user']