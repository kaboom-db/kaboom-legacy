from comics.comics_filters import SeriesFilter
from .models import Series, Issue, Character, Staff, Publisher, StaffPositions
from rest_framework import serializers

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['name', 'logo', 'website', 'id']

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['name', 'alias', 'description', 'image', 'id']

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['name', 'position', 'image', 'id']

class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ['series_name', 'publisher', 'description', 'year_started', 'status', 'id', 'cover_image', 'background_image']

class IssueSerializer(serializers.ModelSerializer):
    characters = CharacterSerializer(read_only=True, many=True)
    staff = StaffSerializer(read_only=True, many=True)
    series = SeriesSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = ['issue_number_absolute', 'issue_number', 'series', 'description', 'characters', 'staff', 'release_date', 'id', 'cover_image']

class StaffPositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffPositions
        fields = ['id', 'position']