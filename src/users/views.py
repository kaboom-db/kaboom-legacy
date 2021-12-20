from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

from users.models import Thought
from users.users_filters import ThoughtFilter

from .serializers import  UserSerializer, ThoughtSerializer, ThoughtTypeSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework import status

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

# TODO: This does not work. Fix it.
class GetThoughts(GenericAPIView):
    serializer_class = ThoughtSerializer
    http_method_names = ['get']
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ThoughtFilter

    def get(self, request):
        thoughts = Thought.objects.all()
        t = ThoughtSerializer(data=thoughts, many=True)
        if t.is_valid():
            return Response(t.data)
        else:
            return Response(t.errors, status=status.HTTP_400_BAD_REQUEST)

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset