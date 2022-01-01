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
        read_only_fields = ['date_created']

class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = '__all__'
        read_only_fields = ['date_created']

class CharacterSerializer(serializers.ModelSerializer):
    voice_actor = VoiceActorSerializer()

    class Meta:
        model = Character
        fields = '__all__'
        read_only_fields = ['date_created']

class SeriesSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    network = NetworkSerializer()
    characters = CharacterSerializer(many=True)
    genres_id = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), write_only=True, many=True)
    characters_id = serializers.PrimaryKeyRelatedField(queryset=Character.objects.all(), write_only=True, many=True)

    class Meta:
        model = Cartoon
        fields = '__all__'
        read_only_fields = ['rating', 'date_created', 'genres', 'characters']
    
    def create(self, validated_data):
        genres = validated_data.pop('genres_id', None)
        characters = validated_data.pop('characters_id', None)
        series = Cartoon.objects.create(**validated_data)
        if genres is not None:
            series.genres.add(*genres)
        if characters is not None:
            series.characters.add(*characters)
        return series

    def update(self, instance, validated_data):
        genres = validated_data.pop('genres_id', None)
        characters = validated_data.pop('characters_id', None)
        instance = super().update(instance, validated_data)

        if genres is not None:
            instance.genres.add(*genres)
        if characters is not None:
            instance.characters.add(*characters)
        instance.save()

        return instance
        

class EpisodeSerializer(serializers.ModelSerializer):
    series = SeriesSerializer()

    class Meta:
        model = Episode
        fields = '__all__'
        read_only_fields = ['date_created']