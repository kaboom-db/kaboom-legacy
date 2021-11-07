from django.db.models import query
from django.http.response import Http404
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

# class GetUserSubscriptions(ModelViewSet):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     serializer_class = ComicSubscriptionSerializer
#     http_method_names = ['get']
# 
#     def get_queryset(self):
#         user = self.request.user
#         return ComicSubscription.objects.filter(user=user.pk)

    # TODO Add a delete method so that users can unsub from a comic
    # def destroy(self, request, pk=None, *args, **kwargs):
    #     try:
    #         user = self.request.user
    #         request.data['user'] = user.pk
    #         serializer = ComicSubscriptionSerializer(data=request.data)
    #         if serializer.is_valid():
    #             sub = ComicSubscription.objects.filter(user=serializer.validated_data['user'], series=serializer.validated_data['series'])
    #             self.perform_destroy(sub)
    #             return Response({'status', 'Successfully unsubscribed'})
    #     except Http404:
    #         pass
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class GetUserSubscriptions(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ComicSubscriptionSerializer
    http_method_names = ['get']

    def get(self, request):
        user = self.request.user
        queryset = ComicSubscription.objects.filter(user=user.pk)
        data = ComicSubscriptionSerializer(queryset, many=True).data
        return Response({'subscriptions': data})
        

class AddUserSubscription(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ComicSubscriptionSerializer
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        user = self.request.user
        request.data['user'] = user.pk
        print(request.data)
        serializer = ComicSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Successfully subscribed'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)