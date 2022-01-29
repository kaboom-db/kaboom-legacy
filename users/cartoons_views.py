from rest_framework.views import APIView

from cartoons.models import Cartoon
from .serializers import CartoonSubscriptionSerializer, CartoonSubscriptionSerializerDetailed, WatchedEpisodesSerializer, WatchedEpisodesSerializerDetailed, UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import CartoonSubscription, ComicSubscription, ReadIssue, WatchedEpisode
from rest_framework import status
from rest_framework import pagination
from django.core.exceptions import ObjectDoesNotExist

### Gets all the cartoons that the user is subbed to
class CartoonSubscriptionsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartoonSubscriptionSerializerDetailed
    http_method_names = ['get', 'post', 'delete']

    def get(self, request):
        user = self.request.user
        # Check if the user specifies a user
        query_user = request.query_params.get('user')
        if query_user:
            user_id = query_user
        else:
            user_id = user.pk
        try:
            queryset = CartoonSubscription.objects.filter(user=user_id).order_by('rating')
            query = request.query_params.get('query')
            if query:
                queryset = CartoonSubscription.objects.filter(user=user_id, series__name__icontains=query).order_by('rating')
            paginator = pagination.PageNumberPagination()
            result_page = paginator.paginate_queryset(queryset, request)
            data = CartoonSubscriptionSerializerDetailed(result_page, many=True).data
            return paginator.get_paginated_response(data)
        except BaseException as e:
            return Response({ 'error': str(e) }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        user = self.request.user
        request.data['user'] = user.pk
        serializer = CartoonSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        user = self.request.user
        request.data['user'] = user.pk
        try:
            instance = CartoonSubscription.objects.filter(user=user.pk, series=request.data['series']).first()
            if instance:
                instance.delete()
                return Response({'success': 'Successfully unsubscribed'})
            else:
                return Response({'error': 'Cannot unsubscribe from a cartoon that has not been subscribed to.'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

### Rate a cartoon
class AddUserSeriesRating(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartoonSubscriptionSerializer
    http_method_names = ['post']

    def post(self, request):
        user = self.request.user
        try:
            instance = CartoonSubscription.objects.filter(user=user.pk, series=request.data['series']).first()
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
                    })
                else:
                    return Response({'error': 'Rating must be between 1 and 10'})
            else:
                return Response({'error': 'Cannot rate a series that has not been subscribed to.'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

### Get all the watched eps of a user
class UserWatchedEpisodesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = WatchedEpisodesSerializerDetailed
    http_method_names = ['get', 'post', 'delete']

    def get(self, request):
        user = self.request.user
        # Check if the user specifies a user
        query_user = request.query_params.get('user')
        if query_user:
            user_id = query_user
        else:
            user_id = user.pk
        try:
            queryset = WatchedEpisode.objects.filter(user=user_id).order_by('-watched_at')
            series = request.query_params.get('series')
            if series:
                queryset = WatchedEpisode.objects.filter(user=user_id, episode__series=series).order_by('-watched_at')
            paginator = pagination.PageNumberPagination()
            result_page = paginator.paginate_queryset(queryset, request)
            data = WatchedEpisodesSerializerDetailed(result_page, many=True).data
            return paginator.get_paginated_response(data)
        except BaseException as ve:
            return Response({ 'error': str(ve) }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        user = self.request.user
        request.data['user'] = user.pk
        serializer = WatchedEpisodesSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Watched the episode'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        user = self.request.user
        request.data['user'] = user.pk
        try:
            instance = WatchedEpisode.objects.get(id=request.data['watched_id'])
            if instance.user == user:
                instance.delete()
                return Response({'success': 'Unwatched the episode'})
            else:
                return Response({'error': 'This watched state does not correspond to the correct user'}, status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

### Remove all watched states of a certain episode
class CleanUserWatchedEpisodes(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = WatchedEpisodesSerializer
    http_method_names = ['delete']

    def delete(self, request):
        user = self.request.user
        request.data['user'] = user.pk
        try:
            instances = WatchedEpisode.objects.filter(episode=request.data['episode'], user=user)
            if instances:
                for instance in instances:
                    instance.delete()
                return Response({'success': 'All watched states have been removed from this episode.'})
            else:
                return Response({'error': 'That episode has not been watched.'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)