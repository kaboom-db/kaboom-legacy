from django_filters import rest_framework as filters
from users.models import UserData
from django.contrib.auth.models import User

class UserFilter(filters.FilterSet):
    username = filters.filters.CharFilter(field_name='username', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['username']