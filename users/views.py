from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView
from rest_framework.views import APIView
from users.models import Comment, Follow, Thought, UserLikedThought, UserData
from users.users_filters import ThoughtFilter, UserFilter
from .serializers import UserDataSerializer, ReportSerializer, ImageRequestSerializer, CommentSerializer, ContentTypeSerializer, FollowSerializer, ThoughtSerializer, UserSerializer, ThoughtSerializerDetailed, CommentSerializerDetailed, UserSerializerDetailed
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import pagination

### Creates a user. Must pass an email, password and username.
class CreateUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                token = Token.objects.get(user=serializer.data['id'])
                return Response({
                    'user_id': serializer.data['id'],
                    'username': serializer.data['username'],
                    'token': token.key
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'error': 'You are either missing an email, password or username. Missing: ' + str(e.args)}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as be:
            return Response({'error': str(be)}, status=status.HTTP_400_BAD_REQUEST)

class GetUsersView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializerDetailed
    http_method_names = ['get']
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter
    queryset = User.objects.filter(userdata__private=False).order_by('-date_joined')

class SpecificUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializerDetailed
    http_method_names = ['get', 'patch']

    def get(self, request, username):
        user = User.objects.filter(username=username, userdata__private=False).first()
        if user:
            serializer = UserSerializerDetailed(instance=user)
            return Response(serializer.data)
        else:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, username):
        current_user = self.request.user
        user_data = UserData.objects.filter(user__username = username).first()
        if user_data:
            # Check if the user is the right user
            if current_user == user_data.user:
                serializer = UserDataSerializer(instance=user_data, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.update(instance=user_data, validated_data=serializer.validated_data)
                    updated_user = UserSerializerDetailed(instance=current_user)
                    return Response(updated_user.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'You are not authorized to edit this user.'}, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

class GetThoughtTypes(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ContentTypeSerializer
    http_method_names = ['get']
    queryset = ContentType.objects.filter(model__in=['comic', 'issue', 'cartoon', 'episode']).order_by('id')

### Get thoughts. Can be filtered with query params
class GetThoughts(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ThoughtSerializerDetailed
    http_method_names = ['get']
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ThoughtFilter
    queryset = Thought.objects.all().order_by('-date_created')

class SpecificThoughtView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ThoughtSerializerDetailed
    http_method_names = ['get', 'delete', 'post']

    def get(self, request, thought_id):
        try:
            thought = Thought.objects.get(id=thought_id)
            serializer = ThoughtSerializerDetailed(thought)
            return Response(serializer.data)
        except:
            return Response({'error': 'Thought Id not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, thought_id):
        user = self.request.user
        try:
            instance = Thought.objects.get(id=thought_id)
            if instance.user == user:
                instance.delete()
                return Response({'success': 'Thought has successfully been deleted.'})
            else:
                return Response({'error': 'This thought does not correspond to the correct user'}, status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, thought_id):
        # A user can only edit their own thought
        user = self.request.user
        try:
            thought = Thought.objects.get(id=thought_id)
            if thought.user == user:
                ### Override the users input of num_of_likes, date created and user
                request.data['num_of_likes'] = thought.num_of_likes
                request.data['date_created'] = thought.date_created
                request.data['user'] = thought.user.id
                serializer = ThoughtSerializer(instance=thought, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.update(instance=thought, validated_data=serializer.validated_data)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'User does not own this thought'}, status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as e:
            return Response({'error': str(e)})

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
            # This allows developers to send a string instead of the id of content type
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
                return Response({'error': 'Thought owner cannot like their own thought.'}, status=status.HTTP_400_BAD_REQUEST)
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
                    }, status=status.HTTP_201_CREATED)
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

class FollowUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer
    http_method_names = ['post']

    def post(self, request, username):
        user = self.request.user
        try:
            following = User.objects.get(username=username)
            request.data['follower'] = user.id
            request.data['following'] = following.id
            serializer = FollowSerializer(data=request.data)
            if user != following:
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
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

    def post(self, request, username):
        user = self.request.user
        try:
            following = User.objects.get(username=username)
            follow_obj = Follow.objects.filter(follower=user, following=following.id)
            if follow_obj:
                follow_obj.delete()
                return Response({'success': 'Successfully unfollowed'})
            else:
                return Response({'error': 'User has not been followed'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GetUsersFollowers(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request, username):
        # Get all the followers
        try:
            following = User.objects.filter(username=username).first()
            if following.userdata.private == False or following == self.request.user:
                users_followers = Follow.objects.filter(following=following.id, follower__userdata__private=False).values_list('follower', flat=True)
                users = User.objects.filter(id__in=users_followers).order_by('username')
                paginator = pagination.PageNumberPagination()
                result_page = paginator.paginate_queryset(users, request)
                serializer = UserSerializerDetailed(instance=users, many=True)
                return paginator.get_paginated_response(data=serializer.data)
            else:
                return Response({'error': 'User does not exist'}, status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

class GetUsersFollowing(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request, username):
        try:
            follower = User.objects.filter(username=username).first()
            if follower.userdata.private == False or follower == self.request.user:
                users_following = Follow.objects.filter(follower=follower.id, following__userdata__private=False).values_list('following', flat=True)
                users = User.objects.filter(id__in=users_following).order_by('username')
                paginator = pagination.PageNumberPagination()
                result_page = paginator.paginate_queryset(users, request)
                serializer = UserSerializerDetailed(instance=users, many=True)
                return paginator.get_paginated_response(data=serializer.data)
            else:
                return Response({'error': 'User does not exist'}, status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

class CommentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    http_method_names = ['post', 'get']

    # adds a comment
    def post(self, request, thought_id):
        user = self.request.user
        try:
            thought = Thought.objects.get(id=thought_id)
            request.data['thought'] = thought.id
            request.data['user'] = user.id
            comment = CommentSerializer(data=request.data, partial=True)
            if comment.is_valid():
                comment.save()
                return Response(comment.data, status=status.HTTP_201_CREATED)
            else:
                return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # gets all comments for this thought
    def get(self, request, thought_id):
        # Get all the comments related to this thought
        try:
            comments = Comment.objects.filter(thought=thought_id).order_by('-date_created')
            if comments:
                serializer = CommentSerializerDetailed(instance=comments, many=True)
                return Response(serializer.data)
            else:
                return Response({'error': 'No comments found'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SpecificCommentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    http_method_names = ['post', 'get', 'delete']

    # get a comment
    def get(self, request, thought_id, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
            thought = Thought.objects.get(id=thought_id)
            if comment.thought == thought:
                serializer = CommentSerializer(instance=comment)
                return Response(serializer.data)
            else:
                return Response({'error': 'Comment ID does not have relation with Thought ID'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # delete a comment
    def delete(self, request, thought_id, comment_id):
        user = self.request.user
        try:
            comment = Comment.objects.get(id=comment_id)
            thought = Thought.objects.get(id=thought_id)
            if comment.user == user:
                if comment.thought == thought:
                    comment.delete()
                    return Response({'success': 'Comment was deleted'})
                else:
                    return Response({'error': 'Comment ID does not have relation with Thought ID'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Comment does not belong to user'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # update a comment
    def post(self, request, thought_id, comment_id):
        user = self.request.user
        try:
            comment = Comment.objects.get(id=comment_id)
            thought = Thought.objects.get(id=thought_id)
            if comment.user == user:
                if comment.thought == thought:
                    print(request.data)
                    request.data['thought'] = comment.thought.id
                    request.data['date_created'] = comment.date_created
                    request.data['user'] = comment.user.id
                    serializer = CommentSerializer(instance=comment, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.update(instance=comment, validated_data=serializer.validated_data)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'Comment ID does not have relation with Thought ID'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Comment does not belong to user'}, status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ImageRequestView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ImageRequestSerializer
    http_method_names = ['post']

    def post(self, request):
        user = self.request.user
        try: 
            data = request.data.copy()
            data['user'] = user.id
            data['status'] = 'NONE'
            if data.get('image', ''):
                print('image supplied')
                serializer = ImageRequestSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise BaseException('No image provided')
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ReportView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ImageRequestSerializer
    http_method_names = ['post']

    def post(self, request):
        user = self.request.user
        try:
            request.data['user'] = user.id
            request.data['status'] = 'NONE'
            serializer = ReportSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)