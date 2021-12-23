from django_filters import rest_framework as filters
from .models import Character, Episode, Genre, Network, Series, VoiceActor

class SeriesFilter(filters.FilterSet):
    query = filters.filters.CharFilter(field_name='name', lookup_expr='icontains')
    genre = filters.filters.NumberFilter(field_name='genres')
    network = filters.filters.NumberFilter(field_name='network')

    class Meta:
        model = Series
        fields = ['name', 'genres', 'network']

class CharactersFilter(filters.FilterSet):
    query = filters.filters.CharFilter(field_name='name', lookup_expr='icontains')
    voice_actor = filters.filters.NumberFilter(field_name='voice_actor')
    series = filters.filters.NumberFilter(field_name='series')

    class Meta:
        model = Character
        fields = ['name', 'voice_actor', 'series']

class EpisodesFilter(filters.FilterSet):
    query = filters.filters.CharFilter(field_name='name', lookup_expr='icontains')
    series = filters.filters.NumberFilter(field_name='series')
    release_date = filters.filters.DateTimeFilter(field_name='release_date', lookup_expr='date')
    season_number = filters.filters.NumberFilter(field_name='season_number')
    episode_number = filters.filters.NumberFilter(field_name='episode_number')

    class Meta:
        model = Episode
        fields = ['name', 'series', 'release_date', 'season_number', 'episode_number']

class GenresFilter(filters.FilterSet):
    query = filters.filters.CharFilter(field_name='genre', lookup_expr='icontains')

    class Meta:
        model = Genre
        fields = ['genre']

class NetworksFilter(filters.FilterSet):
    query = filters.filters.CharFilter(field_name='name', lookup_expr='icontains')
    website = filters.filters.CharFilter(field_name='website', lookup_expr='icontains')

    class Meta:
        model = Network
        fields = ['name', 'website']

class VoiceActorsFilter(filters.FilterSet):
    query = filters.filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = VoiceActor
        fields = ['name']