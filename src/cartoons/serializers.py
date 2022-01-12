from typing import NewType
from .models import Cartoon, Character, Episode, Genre, Network, VoiceActor
from rest_framework import serializers

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class VoiceActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceActor
        fields = '__all__'
        read_only_fields = ['date_created', 'image']

class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = '__all__'
        read_only_fields = ['date_created', 'logo']

class CharacterSerializer(serializers.ModelSerializer):
    voice_actor = VoiceActorSerializer(required=False)
    voice_actor_id = serializers.PrimaryKeyRelatedField(queryset=VoiceActor.objects.all(), write_only=True, required=False)

    class Meta:
        model = Character
        fields = '__all__'
        read_only_fields = ['date_created', 'voice_actor', 'image']
    
    def create(self, validated_data):
        voice_actor = validated_data.pop('voice_actor_id', None)
        character = Character.objects.create(**validated_data)
        if voice_actor is not None:
            character.voice_actor = voice_actor
        character.save()
        return character
    
    def update(self, instance, validated_data):
        voice_actor = validated_data.pop('voice_actor_id', None)
        instance = super().update(instance, validated_data)

        if voice_actor is not None:
            instance.voice_actor = voice_actor
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
    class Meta:
        model = Episode
        fields = '__all__'
        read_only_fields = ['date_created', 'screenshot']