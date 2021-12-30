from functools import partial
from django.contrib.auth.models import User
from django.db.models import base, query
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from cartoons import serializers

from users.models import Comment, Follow, Thought, UserLikedThought
from users.users_filters import ThoughtFilter

from .serializers import  CommentSerializer, ContentTypeSerializer, FollowSerializer, GetFollowersSerializer, GetFollowingsSerializer, ThoughtSerializer, UserSerializer, ThoughtSerializerDetailed, CommentSerializerDetailed, UserSerializerNoPassword
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType

### Creates a user. Must pass an email, password and username.
class CreateUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        print(request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({
                    'user_id': serializer.data['id'],
                    'username': serializer.data['username']
                })
        except KeyError as e:
            raise ParseError(detail='You are either missing an email, password or username. Missing: ' + str(e.args))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetThoughtTypes(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ContentTypeSerializer
    http_method_names = ['get']
    queryset = ContentType.objects.filter(model__in=['comic', 'issue', 'cartoon', 'episode'])

### Get thoughts. Can be filtered with query params
class GetThoughts(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ThoughtSerializerDetailed
    http_method_names = ['get']
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ThoughtFilter
    queryset = Thought.objects.all()

class GetThought(APIView):
    serializer_class = ThoughtSerializer
    http_method_names = ['get']

    def get(self, request, thought_id):
        try:
            thought = Thought.objects.get(id=thought_id)
            serializer = ThoughtSerializer(thought)
            return Response(serializer.data)
        except:
            return Response({'error': 'Thought Id not found'}, status=status.HTTP_404_NOT_FOUND)

### Add a thought
class AddThought(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ThoughtSerializer
    http_method_names = ['post']

    def post(self, request):
        user = self.request.user
        request.data['user'] = user.pk
        try:
            thought_type = request.data['thought_type']
            content_type = ContentType.objects.filter(model=thought_type).first()
            if content_type:
                request.data['thought_type'] = content_type.id
            else:
                return Response({'error': 'Thought type ' + request.data['thought_type'] + ' does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            print('No thought type')
        print(request.data)
        serializer = ThoughtSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

### Remove a thought
class RemoveThought(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ThoughtSerializer
    http_method_names = ['post']

    def post(self, request, thought_id):
        user = self.request.user
        try:
            instance = Thought.objects.get(id=thought_id)
            if instance.user == user:
                instance.delete()
                return Response({'success': 'Thought has successfully been deleted.'})
            else:
                return Response({'thought_id': [
                    'This thought does not correspond to the correct user'
                ]}, status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

### Adds a like to a thought
class LikeThought(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ThoughtSerializer
    http_method_names = ['post']

    def post(self, request, thought_id):
        user = self.request.user
        try:
            instance = Thought.objects.get(id=thought_id)
            ### add one like 
            if instance.user == user:
                # cant like your own thought
                return Response({'thought_id': [
                    'Thought owner cannot like their own thought.'
                ]}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # check if the user has already liked this thought
                already_existing_obj = UserLikedThought.objects.filter(user=user, thought=instance).first()
                if already_existing_obj:
                    return Response({'error': 'This user has already liked this thought'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # create a new liked thought record
                    liked_thought = UserLikedThought(user=user, thought=instance)
                    liked_thought.save()
                    return Response({
                        'thought': instance.id,
                        'num_of_likes': instance.num_of_likes
                    })
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UnlikeThought(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ThoughtSerializer
    http_method_names = ['post']

    def post(self, request, thought_id):
        user = self.request.user
        ### Get the related user thought like object
        user_like = UserLikedThought.objects.filter(user=user, thought=thought_id)
        if user_like:
            ## delete the user like
            user_like.delete()
            return Response({'success': 'Unliked the thought'})
        else:
            return Response({'error': 'User has not liked the thought'}, status=status.HTTP_400_BAD_REQUEST)

class EditThought(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ThoughtSerializer
    http_method_names = ['post']
    
    def post(self, request, thought_id):
        # A user can only edit their own thought
        user = self.request.user
        try:
            thought = Thought.objects.get(id=thought_id)
            if thought.user == user:
                ### Override the users input of num_of_likes, date created and user
                request.data['num_of_likes'] = thought.num_of_likes
                request.data['date_created'] = thought.date_created
                request.data['user'] = thought.user
                serializer = ThoughtSerializer(instance=thought, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.update(instance=thought, validated_data=serializer.validated_data)
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)})

class FollowUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer
    http_method_names = ['post']

    def post(self, request, user_id):
        user = self.request.user
        try:
            following = User.objects.get(id=user_id)
            request.data['follower'] = user.id
            request.data['following'] = following.id
            serializer = FollowSerializer(data=request.data)
            if user != following:
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Users cannot follow themselves'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UnfollowUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer
    http_method_names = ['post']

    def post(self, request, user_id):
        user = self.request.user
        try:
            follow_obj = Follow.objects.filter(follower=user, following=user_id)
            if follow_obj:
                follow_obj.delete()
                return Response({'success': 'Successfully unfollowed'})
            else:
                return Response({'error': 'User has not been followed'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GetUsersFollowers(APIView):
    serializer_class = GetFollowersSerializer
    http_method_names = ['get']

    def get(self, request, user_id):
        # Get all the followers
        users_followers = Follow.objects.filter(following=user_id)
        if users_followers:
            serializer = GetFollowersSerializer(instance=users_followers, many=True)
            return Response(serializer.data)
        else:
            # user has no followers, loner
            return Response({'error': 'User has no followers'}, status=status.HTTP_400_BAD_REQUEST)

class GetUsersFollowing(APIView):
    serializer_class = GetFollowersSerializer
    http_method_names = ['get']

    def get(self, request, user_id):
        users_following = Follow.objects.filter(follower=user_id)
        if users_following:
            serializer = GetFollowingsSerializer(instance=users_following, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'User isn\'t following anyone'}, status=status.HTTP_400_BAD_REQUEST)

class AddComment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    http_method_names = ['post', 'get']

    def post(self, request, thought_id):
        user = self.request.user
        try:
            thought = Thought.objects.get(id=thought_id)
            request.data['thought'] = thought.id
            request.data['user'] = user.id
            comment = CommentSerializer(data=request.data, partial=True)
            if comment.is_valid():
                comment.save()
                return Response(comment.data)
            else:
                return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, thought_id):
        # Get all the comments related to this thought
        try:
            comments = Comment.objects.filter(thought=thought_id)
            if comments:
                serializer = CommentSerializerDetailed(instance=comments, many=True)
                return Response(serializer.data)
            else:
                return Response({'error': 'No comments found'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
