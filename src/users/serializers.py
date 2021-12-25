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
        fields = '__all__'

class ComicSubscriptionSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerNoPassword(read_only=True)
    series = comics_ser.SeriesSerializer(read_only=True)

    class Meta:
        model = ComicSubscription
        fields = '__all__'

class ReadIssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadIssue
        fields = '__all__'

class ReadIssuesSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerNoPassword(read_only=True)
    issue = comics_ser.IssueSerializer(read_only=True)

    class Meta:
        model = ReadIssue
        fields = '__all__'

class CartoonSubscriptionSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerNoPassword(read_only=True)
    series = cartoons_ser.SeriesSerializer(read_only=True)

    class Meta:
        model = CartoonSubscription
        fields = '__all__'

class CartoonSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartoonSubscription
        fields = '__all__'

class WatchedEpisodesSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerNoPassword(read_only=True)
    episode = cartoons_ser.EpisodeSerializer(read_only=True)

    class Meta:
        model = WatchedEpisode
        fields = '__all__'

class WatchedEpisodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchedEpisode
        fields = '__all__'

class ThoughtTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThoughtType
        fields = '__all__'

class ThoughtSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerNoPassword(read_only=True)
    thought_type = ThoughtTypeSerializer(read_only=True)
    comic = comics_ser.SeriesSerializer(read_only=True)
    issue = comics_ser.IssueSerializer(read_only=True)
    cartoon = cartoons_ser.SeriesSerializer(read_only=True)
    episode = cartoons_ser.EpisodeSerializer(read_only=True)

    class Meta:
        model = Thought
        fields = '__all__'

class CommentSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerNoPassword(read_only=True)
    thought = ThoughtSerializerDetailed(read_only=True)

    class Meta:
        model = Comment
        field = '__all__'

class ThoughtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thought
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        field = '__all__'