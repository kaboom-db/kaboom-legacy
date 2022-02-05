from django_filters import rest_framework as filters
from .models import Character, Episode, Genre, Network, Cartoon, VoiceActor

class SeriesFilter(filters.FilterSet):
    query = filters.filters.CharFilter(field_name='name', lookup_expr='icontains')
    genre = filters.filters.CharFilter(field_name='genres', lookup_expr='genre__iexact')
    network = filters.filters.NumberFilter(field_name='network')

    class Meta:
        model = Cartoon
        fields = ['name', 'genres', 'network']

class CharactersFilter(filters.FilterSet):
    query = filters.filters.CharFilter(field_name='name', lookup_expr='icontains')
    alias = filters.filters.CharFilter(field_name='alias', lookup_expr='icontains')
    voice_actors = filters.filters.NumberFilter(field_name='voice_actor')

    class Meta:
        model = Character
        fields = ['name', 'voice_actors', 'alias']

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