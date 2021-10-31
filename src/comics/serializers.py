from .models import Series, Issue, Character, Staff, Publisher
from rest_framework import serializers

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['name', 'logo', 'website', 'id']