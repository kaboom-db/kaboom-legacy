from rest_framework.views import APIView
from .serializers import ComicSubscriptionSerializer, ComicSubscriptionSerializerDetailed, ReadIssuesSerializer, ReadIssuesSerializerDetailed, UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import ComicSubscription, ReadIssue
from rest_framework import status
from rest_framework import pagination
from django.core.exceptions import ObjectDoesNotExist

class CreateUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
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

class GetUserSubscriptions(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ComicSubscriptionSerializerDetailed
    http_method_names = ['get']
    
    def get(self, request):
        user = self.request.user
        queryset = ComicSubscription.objects.filter(user=user.pk)
        query = request.query_params.get('query')
        if query:
            queryset = ComicSubscription.objects.filter(user=user.pk, series__series_name__contains=query)
        paginator = pagination.PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        data = ComicSubscriptionSerializerDetailed(result_page, many=True).data
        return paginator.get_paginated_response(data)
        

class AddUserSubscription(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ComicSubscriptionSerializer
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        user = self.request.user
        request.data['user'] = user.pk
        serializer = ComicSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Successfully subscribed'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RemoveUserSubscription(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ComicSubscriptionSerializer
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        user = self.request.user
        request.data['user'] = user.pk
        try:
            instance = ComicSubscription.objects.filter(user=user.pk, series=request.data['series']).first()
            if instance:
                instance.delete()
                return Response({'status': 'Successfully unsubscribed'})
            else:
                return Response({'series': [
                    'Cannot unsubscribe from a comic that has not been subscribed to.'
                ]}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'series': [
                'This is a required field'
            ]}, status=status.HTTP_400_BAD_REQUEST)

class GetUserReadIssues(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ReadIssuesSerializerDetailed
    http_method_names = ['get']

    def get(self, request):
        user = self.request.user
        queryset = ReadIssue.objects.filter(user=user.pk)
        series = request.query_params.get('series_id')
        if series:
            queryset = ReadIssue.objects.filter(user=user.pk, issue__series=series)
        paginator = pagination.PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        data = ReadIssuesSerializerDetailed(result_page, many=True).data
        return paginator.get_paginated_response(data)

class AddUserReadIssue(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ReadIssuesSerializer
    http_method_names = ['post']

    def post(self, request):
        user = self.request.user
        request.data['user'] = user.pk
        serializer = ReadIssuesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Read the issue'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RemoveUserReadIssue(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ReadIssuesSerializer
    http_method_names = ['post']

    def post(self, request):
        user = self.request.user
        request.data['user'] = user.pk
        try:
            instance = ReadIssue.objects.get(id=request.data['read_id'])
            instance.delete()
            return Response({'status': 'Unread the issue'})
        except KeyError:
            return Response({'read_id': [
                'This is a required field'
            ]}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'issue': [
                'Cannot unread a comic that has not been read.'
            ]}, status=status.HTTP_400_BAD_REQUEST)

class CleanUserReadIssues(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ReadIssuesSerializer
    http_method_names = ['post']

    def post(self, request):
        user = self.request.user
        request.data['user'] = user.pk
        try:
            instances = ReadIssue.objects.filter(issue=request.data['issue'])
            if instances:
                for instance in instances:
                    instance.delete()
                return Response({'status': 'All read states have been removed from this issue.'})
            else:
                return Response({'issue': [
                    'That issue has not been read.'
                ]}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'issue': [
                'This is a required field'
            ]}, status=status.HTTP_400_BAD_REQUEST)