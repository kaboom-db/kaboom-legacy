from comics.comics_filters import SeriesFilter
from .models import Comic, Format, Issue, Character, Staff, Publisher, StaffPositions
from rest_framework import serializers

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

class SeriesSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer(read_only=True)

    class Meta:
        model = Comic
        fields = '__all__'
        read_only_fields = ['rating']

class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = '__all__'

class IssueSerializer(serializers.ModelSerializer):
    characters = CharacterSerializer(read_only=True, many=True)
    staff = StaffSerializer(read_only=True, many=True)
    series = SeriesSerializer(read_only=True)
    format = FormatSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = '__all__'

class StaffPositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffPositions
        fields = '__all__'