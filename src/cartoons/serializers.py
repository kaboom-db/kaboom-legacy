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

class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = '__all__'

class CharacterSerializer(serializers.ModelSerializer):
    voice_actor = VoiceActorSerializer(read_only=True)

    class Meta:
        model = Character
        fields = '__all__'

class SeriesSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(read_only=True, many=True)
    network = NetworkSerializer(read_only=True)
    characters = CharacterSerializer(read_only=True, many=True)

    class Meta:
        model = Cartoon
        fields = '__all__'
        read_only_fields = ['rating']

class EpisodeSerializer(serializers.ModelSerializer):
    series = SeriesSerializer(read_only=True)

    class Meta:
        model = Episode
        fields = '__all__'