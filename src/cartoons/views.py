from .cartoons_filters import SeriesFilter
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