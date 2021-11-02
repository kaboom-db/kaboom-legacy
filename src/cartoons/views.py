from .cartoons_filters import CartoonFilter
from .models import Cartoon, Character, Episode, Genre, Network, VoiceActor
from rest_framework import viewsets
from rest_framework_api_key.permissions import HasAPIKey
from django.db.models import Q
from django_filters import rest_framework as filters
from .serializers import CartoonSerializer, CharacterSerializer, EpisodeSerializer, GenreSerializer, NetworkSerializer, VoiceActorSerializer

class CartoonView(viewsets.ReadOnlyModelViewSet):
    queryset = Cartoon.objects.all()
    serializer_class = CartoonSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CartoonFilter