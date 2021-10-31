from .models import Series, Issue, Character, Staff, Publisher
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

class IssueSerializer(serializers.ModelSerializer):
    characters = CharacterSerializer(read_only=True, many=True)
    staff = StaffSerializer(read_only=True, many=True)

    class Meta:
        model = Issue
        fields = ['issue_number_absolute', 'issue_number', 'series', 'description', 'characters', 'staff', 'release_date', 'id', 'image_small', 'image_medium', 'image_large']