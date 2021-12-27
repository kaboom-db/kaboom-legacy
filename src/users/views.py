from functools import partial
from django.core.checks.messages import Error
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView, set_rollback

from users.models import Thought, ThoughtType
from users.users_filters import ThoughtFilter

from .serializers import  ThoughtSerializer, UserSerializer, ThoughtSerializerDetailed, ThoughtTypeSerializer, CommentSerializerDetailed
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
            raise ParseError(detail='You are either missing an email, password or username. ' + str(e.args))
        return Response({
            serializer.errors
        })

### Get all the thought types
class GetThoughtTypes(ListAPIView):
    serializer_class = ThoughtTypeSerializer
    http_method_names = ['get']
    queryset = ThoughtType.objects.all()

### Get thoughts. Can be filtered with query params
class GetThoughts(ListAPIView):
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
        except KeyError:
            return Response({'thought_id': [
                'This is a required field'
            ]}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'thought': [
                'That thought does not exist.'
            ]}, status=status.HTTP_400_BAD_REQUEST)

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
                instance.num_of_likes += 1
                instance.save()
                return Response({
                    'id': instance.id,
                    'num_of_likes': instance.num_of_likes
                })
        except KeyError:
            return Response({'thought_id': [
                'This is a required field'
            ]}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'thought': [
                'That thought does not exist.'
            ]}, status=status.HTTP_400_BAD_REQUEST)

class EditThought(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ThoughtSerializer
    http_method_names = ['post']

    ### TODO: Add type validations.
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