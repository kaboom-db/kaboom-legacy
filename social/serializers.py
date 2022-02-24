from rest_framework import serializers
from users.serializers import UserSerializerDetailed
from .models import Thought, Comment

class ThoughtSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerDetailed(read_only=True)

    class Meta:
        model = Thought
        fields = '__all__'
        read_only_fields = ['date_created', 'num_of_likes']

class CommentSerializerDetailed(serializers.ModelSerializer):
    user = UserSerializerDetailed(read_only=True)

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