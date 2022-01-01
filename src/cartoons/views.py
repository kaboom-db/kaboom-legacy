from functools import partial
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from .cartoons_filters import CharactersFilter, EpisodesFilter, GenresFilter, NetworksFilter, SeriesFilter, VoiceActorsFilter
from .models import Cartoon, Character, Episode, Genre, Network, VoiceActor
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django_filters import rest_framework as filters
from .serializers import EpisodeSerializerSave, SeriesSerializer, CharacterSerializer, EpisodeSerializer, GenreSerializer, NetworkSerializer, VoiceActorSerializer
from rest_framework import pagination

class AllowGetAuthentication(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return super(AllowGetAuthentication, self).has_permission(request, view)

class SeriesView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowGetAuthentication]
    serializer_class = SeriesSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SeriesFilter
    http_method_names = ['get', 'post', 'patch']

    def list(self, request):
        queryset = Cartoon.objects.all().order_by('name')
        queryset = self.filter_queryset(queryset=queryset)
        paginator = pagination.PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = SeriesSerializer(instance=result_page, many=True)
        return paginator.get_paginated_response(data=serializer.data)

    def create(self, request):
        if request.data:
            serializer = SeriesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Request body must not be empty'}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        try:
            series = Cartoon.objects.get(pk=pk)
            serializer = SeriesSerializer(instance=series)
            return Response(serializer.data)
        except:
            return Response({'error': 'Cartoon with ID does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            series = Cartoon.objects.get(pk=pk)
            if request.data:
                serializer = SeriesSerializer(instance=series, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.update(instance=series, validated_data=serializer.validated_data)
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Request body must not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CharacterView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowGetAuthentication]
    serializer_class = CharacterSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CharactersFilter
    http_method_names = ['get', 'post', 'patch']

    def list(self, request):
        queryset = Character.objects.all().order_by('name')
        queryset = self.filter_queryset(queryset)
        paginator = pagination.PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = CharacterSerializer(instance=result_page, many=True)
        return paginator.get_paginated_response(data=serializer.data)
    
    def create(self, request):
        if request.data:
            serializer = CharacterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Request body must not be empty'}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        try:
            character = Character.objects.get(pk=pk)
            serializer = CharacterSerializer(instance=character)
            return Response(serializer.data)
        except:
            return Response({'error': 'Cartoon with ID does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    def partial_update(self, request, pk=None):
        try:
            character = Character.objects.get(pk=pk)
            if request.data:
                serializer = CharacterSerializer(instance=character, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.update(instance=character, validated_data=serializer.validated_data)
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Request body must not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class EpisodeView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowGetAuthentication]
    serializer_class = EpisodeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EpisodesFilter
    http_method_names = ['get', 'post', 'patch']

    def list(self, request):
        queryset = Episode.objects.all().order_by('episode_number')
        queryset = self.filter_queryset(queryset)
        paginator = pagination.PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = EpisodeSerializer(instance=result_page, many=True)
        return paginator.get_paginated_response(data=serializer.data)
    
    def create(self, request):
        try:
            serializer = EpisodeSerializerSave(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        try:
            episode = Episode.objects.get(pk=pk)
            serializer = EpisodeSerializer(instance=episode)
            return Response(serializer.data)
        except:
            return Response({'error': 'Episode with ID does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    def partial_update(self, request, pk=None):
        try:
            episode = Episode.objects.get(pk=pk)
            if request.data:
                serializer = EpisodeSerializerSave(instance=episode, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.update(instance=episode, validated_data=serializer.validated_data)
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Request body must not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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