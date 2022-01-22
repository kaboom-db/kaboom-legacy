from rest_framework import serializers
from django.contrib.auth.models import User
from comics.models import Issue
from users.models import Report, ImageRequest, CartoonSubscription, ComicSubscription, Follow, ReadIssue, WatchedEpisode, Thought, Comment, get_user_image
import comics.serializers as comics_ser
import cartoons.serializers as cartoons_ser
from django.contrib.contenttypes.models import ContentType

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
        fields = ['username', 'password', 'email', 'id']

class UserSerializerDetailed(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image')
    date_joined = serializers.SerializerMethodField('get_date_joined')
    time_joined = serializers.SerializerMethodField('get_time_joined')

    def get_time_joined(self, obj) -> str:
        return str(obj.date_joined.time())

    def get_date_joined(self, obj) -> str:
        return str(obj.date_joined.date())

    def get_image(self, obj) -> str:
        return get_user_image(obj.email)

    class Meta:
        model = User
        fields = ['username', 'id', 'image', 'date_joined', 'time_joined', 'is_admin']

class ComicSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComicSubscription
        fields = '__all__'

class ComicSubscriptionSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerDetailed(read_only=True)
    series = comics_ser.SeriesSerializer(read_only=True)

    class Meta:
        model = ComicSubscription
        fields = '__all__'

class ReadIssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadIssue
        fields = '__all__'

class ReadIssuesSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerDetailed(read_only=True)
    issue = comics_ser.IssueSerializer(read_only=True)

    class Meta:
        model = ReadIssue
        fields = '__all__'

class CartoonSubscriptionSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerDetailed(read_only=True)
    series = cartoons_ser.SeriesSerializer(read_only=True)

    class Meta:
        model = CartoonSubscription
        fields = '__all__'

class CartoonSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartoonSubscription
        fields = '__all__'

class WatchedEpisodesSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerDetailed(read_only=True)
    episode = cartoons_ser.EpisodeSerializer(read_only=True)

    class Meta:
        model = WatchedEpisode
        fields = '__all__'

class WatchedEpisodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchedEpisode
        fields = '__all__'

class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ['id', 'model']
        lookup_field = 'model'

class ThoughtSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerDetailed(read_only=True)
    thought_type = ContentTypeSerializer(read_only=True)

    class Meta:
        model = Thought
        fields = '__all__'
        read_only_fields = ['date_created', 'num_of_likes']

class CommentSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerDetailed(read_only=True)
    thought = ThoughtSerializerDetailed(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['date_created']

class ThoughtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thought
        fields = '__all__'
        read_only_fields = ['date_created', 'num_of_likes']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['date_created']

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

class GetFollowersSerializer(serializers.ModelSerializer):
    follower = UserSerializerDetailed(read_only=True)

    class Meta:
        model = Follow
        fields = ['follower']

class GetFollowingsSerializer(serializers.ModelSerializer):
    following = UserSerializerDetailed(read_only=True)

    class Meta:
        model = Follow
        fields = ['following']

class ImageRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageRequest
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'