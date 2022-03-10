from django_filters import rest_framework as filters
from .models import Character, Episode, Genre, Network, Cartoon, VoiceActor, Team, Location

class SeriesFilter(filters.FilterSet):
    query = filters.filters.CharFilter(field_name='name', lookup_expr='icontains')
    genre = filters.filters.CharFilter(field_name='genres', lookup_expr='genre__iexact')
    network = filters.filters.NumberFilter(field_name='network')
    status = filters.filters.CharFilter(field_name='status', lookup_expr='icontains')

    class Meta:
        model = Cartoon
        fields = ['name', 'genres', 'network', 'status']

class CharactersFilter(filters.FilterSet):
    query = filters.filters.CharFilter(field_name='name', lookup_expr='icontains')
    alias = filters.filters.CharFilter(field_name='alias', lookup_expr='icontains')
    voice_actors = filters.filters.NumberFilter(field_name='voice_actors')

    class Meta:
        model = Character
        fields = ['name', 'voice_actors', 'alias']

class EpisodesFilter(filters.FilterSet):
    query = filters.filters.CharFilter(field_name='name', lookup_expr='icontains')
    series = filters.filters.NumberFilter(field_name='series')
    # // TODO: Document new filters on both cartoon_filters and comics_filters
    # //    Docs for the date filters are out of date
    release_date = filters.filters.DateFromToRangeFilter(field_name='release_date')
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

class TeamFilter(filters.FilterSet):
    query = filters.filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Team
        fields = ['name']

class LocationFilter(filters.FilterSet):
    city = filters.filters.CharFilter(field_name='city', lookup_expr='icontains')
    nation = filters.filters.CharFilter(field_name='nation', lookup_expr='icontains')

    class Meta:
        model = Location
        fields = ['city', 'nation']