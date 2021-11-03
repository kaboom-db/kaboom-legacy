from .cartoons_filters import CharactersFilter, EpisodesFilter, SeriesFilter
from .models import Series, Character, Episode, Genre, Network, VoiceActor
from rest_framework import viewsets
from rest_framework_api_key.permissions import HasAPIKey
from django.db.models import Q
from django_filters import rest_framework as filters
from .serializers import SeriesSerializer, CharacterSerializer, EpisodeSerializer, GenreSerializer, NetworkSerializer, VoiceActorSerializer

class SeriesView(viewsets.ReadOnlyModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SeriesFilter

class CharacterView(viewsets.ReadOnlyModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CharactersFilter

class EpisodeView(viewsets.ReadOnlyModelViewSet):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EpisodesFilter