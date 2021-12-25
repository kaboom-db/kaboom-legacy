from .cartoons_filters import CharactersFilter, EpisodesFilter, GenresFilter, NetworksFilter, SeriesFilter, VoiceActorsFilter
from .models import Cartoon, Character, Episode, Genre, Network, VoiceActor
from rest_framework import viewsets
from django.db.models import Q
from django_filters import rest_framework as filters
from .serializers import SeriesSerializer, CharacterSerializer, EpisodeSerializer, GenreSerializer, NetworkSerializer, VoiceActorSerializer

class SeriesView(viewsets.ReadOnlyModelViewSet):
    queryset = Cartoon.objects.all()
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

class GenreView(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = GenresFilter

class NetworkView(viewsets.ReadOnlyModelViewSet):
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NetworksFilter

class VoiceActorView(viewsets.ReadOnlyModelViewSet):
    queryset = VoiceActor.objects.all()
    serializer_class = VoiceActorSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = VoiceActorsFilter