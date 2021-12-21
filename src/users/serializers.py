from rest_framework import serializers
from django.contrib.auth.models import User
from comics.models import Issue
from users.models import CartoonSubscription, ComicSubscription, ReadIssue, WatchedEpisode, ThoughtType, Thought, Comment
import comics.serializers as comics_ser
import cartoons.serializers as cartoons_ser

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
        fields = ['username', 'id']

class ComicSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComicSubscription
        fields = ['series', 'user', 'rating']

class ComicSubscriptionSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerNoPassword(read_only=True)
    series = comics_ser.SeriesSerializer(read_only=True)

    class Meta:
        model = ComicSubscription
        fields = ['series', 'user', 'rating']

class ReadIssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadIssue
        fields = ['issue', 'user', 'read_at']

class ReadIssuesSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerNoPassword(read_only=True)
    issue = comics_ser.IssueSerializer(read_only=True)

    class Meta:
        model = ReadIssue
        fields = ['issue', 'user', 'read_at', 'id']

class CartoonSubscriptionSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerNoPassword(read_only=True)
    series = cartoons_ser.SeriesSerializer(read_only=True)

    class Meta:
        model = CartoonSubscription
        fields = ['series', 'user', 'rating']

class CartoonSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartoonSubscription
        fields = ['series', 'user', 'rating']

class WatchedEpisodesSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerNoPassword(read_only=True)
    episode = cartoons_ser.EpisodeSerializer(read_only=True)

    class Meta:
        model = WatchedEpisode
        fields = ['episode', 'user', 'watched_at', 'id']

class WatchedEpisodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchedEpisode
        fields = ['episode', 'user', 'watched_at', 'id']

class ThoughtTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThoughtType
        fields = ['name', 'id']

class ThoughtSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerNoPassword(read_only=True)
    thought_type = ThoughtTypeSerializer(read_only=True)
    comic = comics_ser.SeriesSerializer(read_only=True)
    issue = comics_ser.IssueSerializer(read_only=True)
    cartoon = cartoons_ser.SeriesSerializer(read_only=True)
    episode = cartoons_ser.EpisodeSerializer(read_only=True)

    class Meta:
        model = Thought
        fields = ['user', 'post_content', 'date_created', 'thought_type', 'comic', 'issue', 'cartoon', 'episode', 'num_of_likes']

class CommentSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerNoPassword(read_only=True)
    thought = ThoughtSerializerDetailed(read_only=True)

    class Meta:
        model = Comment
        field = ['user', 'comment_content', 'date_created', 'thought']

class ThoughtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thought
        fields = ['user', 'post_content', 'date_created', 'thought_type', 'comic', 'issue', 'cartoon', 'episode', 'num_of_likes']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        field = ['user', 'comment_content', 'date_created', 'thought']