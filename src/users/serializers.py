from rest_framework import serializers
from django.contrib.auth.models import User
from comics.models import Issue
from users.models import CartoonSubscription, ComicSubscription, ReadIssue, WatchedEpisode
from comics.serializers import IssueSerializer, SeriesSerializer
import cartoons.serializers

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'id']

class UserSerializerNoPassword(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'id']

class ComicSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComicSubscription
        fields = ['series', 'user', 'rating']

class ComicSubscriptionSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerNoPassword(read_only=True)
    series = SeriesSerializer(read_only=True)

    class Meta:
        model = ComicSubscription
        fields = ['series', 'user', 'rating']

class ReadIssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadIssue
        fields = ['issue', 'user', 'read_at']

class ReadIssuesSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerNoPassword(read_only=True)
    issue = IssueSerializer(read_only=True)

    class Meta:
        model = ReadIssue
        fields = ['issue', 'user', 'read_at', 'id']

class CartoonSubscriptionSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerNoPassword(read_only=True)
    series = cartoons.serializers.SeriesSerializer(read_only=True)

    class Meta:
        model = CartoonSubscription
        fields = ['series', 'user', 'rating']

class CartoonSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartoonSubscription
        fields = ['series', 'user', 'rating']

class WatchedEpisodesSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerNoPassword(read_only=True)
    episode = cartoons.serializers.EpisodeSerializer(read_only=True)

    class Meta:
        model = WatchedEpisode
        fields = ['episode', 'user', 'watched_at', 'id']

class WatchedEpisodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchedEpisode
        fields = ['episode', 'user', 'watched_at', 'id']