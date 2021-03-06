from rest_framework.response import Response
from .cartoons_filters import CharactersFilter, EpisodesFilter, GenresFilter, NetworksFilter, SeriesFilter, VoiceActorsFilter, TeamFilter, LocationFilter
from .models import Cartoon, Character, Episode, Genre, Network, VoiceActor, Team, Location
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django_filters import rest_framework as filters
from .serializers import LocationSerializer, EpisodeSerializerSave, SeriesSerializer, CharacterSerializer, EpisodeSerializer, GenreSerializer, NetworkSerializer, VoiceActorSerializer, TeamSerializer
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
                return Response(serializer.data, status=status.HTTP_201_CREATED)
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
                return Response(serializer.data, status=status.HTTP_201_CREATED)
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
            return Response({'error': 'Character with ID does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
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
        queryset = Episode.objects.all().order_by('season_number')
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
                return Response(serializer.data, status=status.HTTP_201_CREATED)
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
                # over write data
                request.data['series'] = episode.series.id
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
    queryset = Genre.objects.all().order_by('genre')
    serializer_class = GenreSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = GenresFilter

class NetworkView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowGetAuthentication]
    serializer_class = NetworkSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NetworksFilter
    http_method_names = ['get', 'post', 'patch']

    def list(self, request):
        queryset = Network.objects.all().order_by('name')
        queryset = self.filter_queryset(queryset)
        paginator = pagination.PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = NetworkSerializer(instance=result_page, many=True)
        return paginator.get_paginated_response(data=serializer.data)
    
    def create(self, request):
        try:
            serializer = NetworkSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        try:
            network = Network.objects.get(pk=pk)
            serializer = NetworkSerializer(instance=network)
            return Response(serializer.data)
        except:
            return Response({'error': 'Network with ID does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            network = Network.objects.get(pk=pk)
            if request.data:
                serializer = NetworkSerializer(instance=network, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.update(instance=network, validated_data=serializer.validated_data)
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Request body must not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class VoiceActorView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowGetAuthentication]
    serializer_class = VoiceActorSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = VoiceActorsFilter
    http_method_names = ['get', 'post', 'patch']

    def list(self, request):
        queryset = VoiceActor.objects.all().order_by('name')
        queryset = self.filter_queryset(queryset)
        paginator = pagination.PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = VoiceActorSerializer(instance=result_page, many=True)
        return paginator.get_paginated_response(data=serializer.data)
    
    def create(self, request):
        try:
            serializer = VoiceActorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            actor = VoiceActor.objects.get(pk=pk)
            serializer = VoiceActorSerializer(instance=actor)
            return Response(serializer.data)
        except:
            return Response({'error': 'Actor with ID does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            actor = VoiceActor.objects.get(pk=pk)
            if request.data:
                serializer = VoiceActorSerializer(instance=actor, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.update(instance=actor, validated_data=serializer.validated_data)
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Request body must not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TeamView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowGetAuthentication]
    serializer_class = TeamSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TeamFilter
    http_method_names = ['get', 'post', 'patch']

    def list(self, request):
        queryset = Team.objects.all().order_by('name')
        queryset = self.filter_queryset(queryset)
        paginator = pagination.PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = TeamSerializer(instance=result_page, many=True)
        return paginator.get_paginated_response(data=serializer.data)
    
    def create(self, request):
        try:
            serializer = TeamSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            team = Team.objects.get(pk=pk)
            serializer = TeamSerializer(instance=team)
            return Response(serializer.data)
        except:
            return Response({'error': 'Team with ID does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            team = Team.objects.get(pk=pk)
            if request.data:
                serializer = TeamSerializer(instance=team, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.update(instance=team, validated_data=serializer.validated_data)
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Request body must not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LocationView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowGetAuthentication]
    serializer_class = LocationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LocationFilter
    http_method_names = ['get', 'post', 'patch']

    def list(self, request):
        queryset = Location.objects.all().order_by('-date_created')
        queryset = self.filter_queryset(queryset)
        paginator = pagination.PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = LocationSerializer(instance=result_page, many=True)
        return paginator.get_paginated_response(data=serializer.data)

    def create(self, request):
        try:
            serializer = LocationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            location = Location.objects.get(pk=pk)
            serializer = LocationSerializer(instance=location)
            return Response(serializer.data)
        except:
            return Response({'error': 'Location with ID does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            location = Location.objects.get(pk=pk)
            if request.data:
                serializer = LocationSerializer(instance=location, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.update(instance=location, validated_data=serializer.validated_data)
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Request body must not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
