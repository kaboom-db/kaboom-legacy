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

from django.contrib.auth.models import User

### Gets a users comic subcriptions. Can pass in a query.
class ComicSubscriptionsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ComicSubscriptionSerializerDetailed
    http_method_names = ['get', 'post', 'delete']
    
    def get(self, request):
        user = self.request.user
        # Check if the user specifies a user
        query_user = request.query_params.get('user')
        if query_user:
            user_id = query_user
            # Check if specified user is private
            tmp = User.objects.filter(id=user_id, userdata__private=False).first()
            if not tmp:
                return Response({'error': 'This user either does not exist or is private'})
        else:
            user_id = user.pk
        try:
            queryset = ComicSubscription.objects.filter(user=user_id).order_by('rating')
            query = request.query_params.get('query')
            if query:
                queryset = ComicSubscription.objects.filter(user=user_id, series__series_name__icontains=query).order_by('rating')
            paginator = pagination.PageNumberPagination()
            result_page = paginator.paginate_queryset(queryset, request)
            data = ComicSubscriptionSerializerDetailed(result_page, many=True).data
            return paginator.get_paginated_response(data)
        except BaseException as e:
            return Response({ 'error': str(e) }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        user = self.request.user
        data = request.data.copy()
        data['user'] = user.pk
        serializer = ComicSubscriptionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        user = self.request.user
        try:
            instance = ComicSubscription.objects.filter(user=user.pk, series=request.data['series']).first()
            if instance:
                instance.delete()
                return Response({'success': 'Successfully unsubscribed'})
            else:
                return Response({'error': 'Cannot unsubscribe from a comic that has not been subscribed to.'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
                if int(rating) >= 1 and int(rating) <= 10:
                    instance.rating = rating
                    instance.save()
                    return Response({
                        'series': instance.series.id,
                        'user': instance.user.id,
                        'id': instance.id,
                        'rating': instance.rating
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'Rating must be between 1 and 10'})
            else:
                return Response({'error': 'Cannot rate a series that has not been subscribed to.'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

### Gets all the read issues of the user.
class UserReadIssuesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ReadIssuesSerializerDetailed
    http_method_names = ['get', 'post', 'delete']

    def get(self, request):
        user = self.request.user
        # Check if the user specifies a user
        query_user = request.query_params.get('user')
        if query_user:
            user_id = query_user
            # Check if specified user is private
            tmp = User.objects.filter(id=user_id, userdata__private=False).first()
            if not tmp:
                return Response({'error': 'This user either does not exist or is private'})
        else:
            user_id = user.pk
        try:
            queryset = ReadIssue.objects.filter(user=user_id).order_by('-read_at')
            series = request.query_params.get('series')
            if series:
                queryset = ReadIssue.objects.filter(user=user_id, issue__series=series).order_by('-read_at')
            paginator = pagination.PageNumberPagination()
            result_page = paginator.paginate_queryset(queryset, request)
            data = ReadIssuesSerializerDetailed(result_page, many=True).data
            return paginator.get_paginated_response(data)
        except BaseException as ve:
            return Response({ 'error': str(ve) }, status=status.HTTP_400_BAD_REQUEST)

    ### Adds an issue as read
    def post(self, request):
        user = self.request.user
        data = request.data.copy()
        data['user'] = user.pk
        serializer = ReadIssuesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = self.request.user
        try:
            instance = ReadIssue.objects.get(id=request.data['read_id'])
            ## Check if the instance is attached to the user
            if instance.user == user:
                instance.delete()
                return Response({'success': 'Unread the issue'})
            else:
                return Response({'error': 'This read state does not correspond to the correct user'}, status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

### Removes all read states from the issue
class CleanUserReadIssues(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ReadIssuesSerializer
    http_method_names = ['delete']

    def delete(self, request):
        user = self.request.user
        try:
            instances = ReadIssue.objects.filter(issue=request.data['issue'], user=user)
            if instances:
                for instance in instances:
                    instance.delete()
                return Response({'success': 'All read states have been removed from this issue.'})
            else:
                return Response({'error': 'That issue has not been read.'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)