from .models import Cartoon, Character, Episode, Genre, Network, VoiceActor
from rest_framework import serializers

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre', 'id']

class VoiceActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceActor
        fields = ['name', 'id', 'image']

class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = ['name', 'website', 'id', 'logo']

class CharacterSerializer(serializers.ModelSerializer):
    voice_actor = VoiceActorSerializer(read_only=True)

    class Meta:
        model = Character
        fields = ['name', 'voice_actor', 'id', 'image']

class CartoonSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(read_only=True, many=True)
    network = NetworkSerializer(read_only=True)

    class Meta:
        model = Cartoon
        fields = ['name', 'network', 'genres', 'summary', 'season_count', 'id', 'image_small', 'image_medium', 'image_large']

class EpisodeSerializer(serializers.ModelSerializer):
    cartoon = CartoonSerializer(read_only=True)

    class Meta:
        model = Episode
        fields = ['episode_number', 'absolute_episode_number', 'season_number', 'cartoon', 'name', 'summary', 'release_date', 'rating', 'screenshot', 'id']