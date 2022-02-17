from .models import Cartoon, Character, Episode, Genre, Network, VoiceActor, Team, Location
from rest_framework import serializers
from kaboom.utils import util_calculate_age
from datetime import date
from django.core.exceptions import ValidationError

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class VoiceActorSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField(method_name='calculate_age')

    def calculate_age(self, obj):
        today = date.today()
        if obj.date_of_birth:
            if obj.date_of_death:
                return util_calculate_age(obj.date_of_birth, obj.date_of_death)
            else:
                return util_calculate_age(obj.date_of_birth, today)
        else:
            return None

    class Meta:
        model = VoiceActor
        fields = '__all__'
        read_only_fields = ['date_created', 'image']

class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = '__all__'
        read_only_fields = ['date_created', 'logo']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        read_only_fields = ['date_created', 'logo']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        read_only_fields = ['date_created']

class CharacterSerializer(serializers.ModelSerializer):
    voice_actors = VoiceActorSerializer(required=False, many=True, read_only=True)
    voice_actors_id = serializers.PrimaryKeyRelatedField(queryset=VoiceActor.objects.all(), write_only=True, required=False, many=True)
    teams = TeamSerializer(required=False, many=True, read_only=True)
    teams_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), write_only=True, required=False, many=True)
    location_of_operation = LocationSerializer(required=False, read_only=True)
    location_of_operation_id = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), write_only=True, required=False)

    class Meta:
        model = Character
        fields = '__all__'
        read_only_fields = ['date_created', 'voice_actors', 'image']
    
    def create(self, validated_data):
        voice_actors = validated_data.pop('voice_actors_id', None)
        teams = validated_data.pop('teams_id', None)
        location_of_operation = validated_data.pop('location_of_operation_id', None)
        character = Character.objects.create(**validated_data)
        if voice_actors is not None:
            character.voice_actors.add(*voice_actors)
        if teams is not None:
            character.teams.add(*teams)
        if location_of_operation is not None:
            character.location_of_operation = location_of_operation
        character.save()
        return character
    
    def update(self, instance, validated_data):
        voice_actors = validated_data.pop('voice_actors_id', None)
        teams = validated_data.pop('teams_id', None)
        location_of_operation = validated_data.pop('location_of_operation_id', None)
        instance = super().update(instance, validated_data)
        if voice_actors is not None:
            instance.voice_actors.add(*voice_actors)
        if teams is not None:
            instance.teams.add(*teams)
        if location_of_operation is not None:
            instance.location_of_operation = location_of_operation
        instance.save()
        return instance

class SeriesSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, required=False)
    network = NetworkSerializer(required=False)
    characters = CharacterSerializer(many=True, required=False)
    genres_id = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), write_only=True, many=True, required=False)
    characters_id = serializers.PrimaryKeyRelatedField(queryset=Character.objects.all(), write_only=True, many=True, required=False)
    network_id = serializers.PrimaryKeyRelatedField(queryset=Network.objects.all(), write_only=True, required=False)

    class Meta:
        model = Cartoon
        fields = '__all__'
        read_only_fields = ['rating', 'date_created', 'genres', 'characters', 'network', 'cover_image', 'background_image']
    
    def create(self, validated_data):
        genres = validated_data.pop('genres_id', None)
        characters = validated_data.pop('characters_id', None)
        network = validated_data.pop('network_id', None)
        series = Cartoon.objects.create(**validated_data)
        if genres is not None:
            series.genres.add(*genres)
        if characters is not None:
            series.characters.add(*characters)
        if network is not None:
            series.network = network
        series.save()
        return series

    def update(self, instance, validated_data):
        genres = validated_data.pop('genres_id', None)
        characters = validated_data.pop('characters_id', None)
        network = validated_data.pop('network_id', None)
        instance = super().update(instance, validated_data)

        if genres is not None:
            instance.genres.add(*genres)
        if characters is not None:
            instance.characters.add(*characters)
        if network is not None:
            instance.network = network
        instance.save()

        return instance

class EpisodeSerializer(serializers.ModelSerializer):
    series = SeriesSerializer()

    class Meta:
        model = Episode
        fields = '__all__'
        read_only_fields = ['date_created', 'series', 'screenshot']

class EpisodeSerializerSave(serializers.ModelSerializer):
    def create(self, validated_data):
        print(validated_data['series'].id)
        series = Cartoon.objects.get(pk=validated_data['series'].id)
        print(series)
        if int(validated_data['season_number']) > series.season_count:
            raise ValidationError('Season number does not exist for series ' + str(series))
        else:
            episode = Episode.objects.create(**validated_data)
            return episode

    class Meta:
        model = Episode
        fields = '__all__'
        read_only_fields = ['date_created', 'screenshot']