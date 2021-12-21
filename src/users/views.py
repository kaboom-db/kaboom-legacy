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

    def post(self, request):
        user = self.request.user
        try:
            instance = Thought.objects.get(id=request.data['thought_id'])
            if instance.user == user:
                instance.delete()
                return Response({'status': 'Thought has successfully been deleted.'})
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