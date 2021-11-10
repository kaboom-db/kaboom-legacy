from rest_framework import serializers
from django.contrib.auth.models import User
from comics.models import Issue
from users.models import ComicSubscription, ReadIssue
from comics.serializers import IssueSerializer, SeriesSerializer

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user

    class Meta:
        model = User
        fields = ['username', 'email', 'id']

class ComicSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComicSubscription
        fields = ['series', 'user', 'rating']

class ComicSubscriptionSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    series = SeriesSerializer(read_only=True)

    class Meta:
        model = ComicSubscription
        fields = ['series', 'user', 'rating']

class ReadIssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadIssue
        fields = ['issue', 'user', 'watched_at']

class ReadIssuesSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    issue = IssueSerializer(read_only=True)

    class Meta:
        model = ReadIssue
        fields = ['issue', 'user', 'watched_at', 'id']