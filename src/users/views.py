from django.db.models import query
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.views import APIView
from .serializers import ComicSubscriptionSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import ComicSubscription
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet
from rest_framework import status

class CreateUser(APIView):
    def post(self, request):
        post_data = request.data
        serializer = UserSerializer(data=post_data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({
                    'user_id': serializer.data['id'],
                    'username': serializer.data['username']
                })
        except KeyError:
            raise ParseError(detail='You are either missing an email, password or username.')
        return Response({
            serializer.errors
        })

class GetUserSubscriptions(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ComicSubscriptionSerializer
    http_method_names = ['get', 'post']

    def get_queryset(self):
        user = self.request.user
        return ComicSubscription.objects.filter(user=user.pk)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        request.data['user'] = user.pk
        print(request.data)
        serializer = ComicSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Successfully subscribed'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO Add a delete method so that users can unsub from a comic