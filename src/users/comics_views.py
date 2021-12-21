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

### Gets a users comic subcriptions. Can pass in a query.
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

### Adds a comic series to a users subscription list.
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
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

### Removes a series from the subscription list.
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

### Add a rating to a series.
class AddUserSeriesRating(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ComicSubscriptionSerializer
    http_method_names = ['post']

    def post(self, request):
        user = self.request.user
        try:
            # Get the series from the users list 
            instance = ComicSubscription.objects.filter(user=user.pk, series=request.data['series']).first()
            if instance:
                rating = request.data['rating']
                if int(rating) >= 0 and int(rating) <= 10:
                    instance.rating = rating
                    instance.save()
                    return Response({
                        'series': instance.series.id,
                        'user': instance.user.id,
                        'id': instance.id,
                        'rating': instance.rating
                    })
                else:
                    raise ValueError()
            else:
                return Response({'series': [
                    'Cannot rate a series that has not been subscribed to.'
                ]}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'field_error': [
                'Rating and series are both required fields.'
            ]}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'field_error': [
                'Rating needs to be a number between 0 and 10'
            ]}, status=status.HTTP_400_BAD_REQUEST)

### Gets all the read issues of the user.
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

### Adds an issue as read.
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

### Removes an issue from read.
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
            ## Check if the instance is attached to the user
            if instance.user == user:
                instance.delete()
                return Response({'status': 'Unread the issue'})
            else:
                return Response({'read_id': [
                    'This read state does not correspond to the correct user'
                ]}, status=status.HTTP_401_UNAUTHORIZED)
        except KeyError:
            return Response({'read_id': [
                'This is a required field'
            ]}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'issue': [
                'Cannot unread a comic that has not been read.'
            ]}, status=status.HTTP_400_BAD_REQUEST)

### Removes all read states from the issue
class CleanUserReadIssues(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ReadIssuesSerializer
    http_method_names = ['post']

    def post(self, request):
        user = self.request.user
        request.data['user'] = user.pk
        try:
            instances = ReadIssue.objects.filter(issue=request.data['issue'], user=user)
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