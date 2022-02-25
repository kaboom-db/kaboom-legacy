from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView
from rest_framework.views import APIView
from users.models import Follow, UserData
from users.users_filters import UserFilter
from .serializers import UserDataSerializer, ReportSerializer, ImageRequestSerializer, ContentTypeSerializer, FollowSerializer, UserSerializer, UserSerializerDetailed
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

# // TODO(#5): Optimize with use of select_related
# //    Check this for inspiration: https://sayari3.com/articles/33-what-is-select_related-in-django/

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
