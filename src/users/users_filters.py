from django_filters import rest_framework as filters
from users.models import Thought
from django.contrib.auth.models import User

class ThoughtFilter(filters.FilterSet):
    user = filters.filters.NumberFilter(field_name='user')
    thought_type = filters.filters.NumberFilter(field_name='thought_type')
    comic = filters.filters.NumberFilter(field_name='comic')
    issue = filters.filters.NumberFilter(field_name='issue')
    cartoon = filters.filters.NumberFilter(field_name='cartoon')
    episode = filters.filters.NumberFilter(field_name='episode')
    date_created = filters.filters.DateFromToRangeFilter(field_name='date_created')

    class Meta:
        model = Thought
        fields = ['user', 'thought_type', 'comic', 'issue', 'cartoon', 'episode', 'date_created']

class UserFilter(filters.FilterSet):
    username = filters.filters.CharFilter(field_name='username', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['username']