from rest_framework.views import APIView

from cartoons.models import Series
from .serializers import CartoonSubscriptionSerializer, CartoonSubscriptionSerializerDetailed, ReadIssuesSerializer, ReadIssuesSerializerDetailed, UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import CartoonSubscription, ReadIssue
from rest_framework import status
from rest_framework import pagination
from django.core.exceptions import ObjectDoesNotExist

### Gets all the cartoons that the user is subbed to
class GetUserSubscriptions(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartoonSubscriptionSerializerDetailed
    http_method_names = ['get']

    def get(self, request):
        user = self.request.user
        queryset = CartoonSubscription.objects.filter(user=user.pk)
        query = request.query_params.get('query')
        if query:
            queryset = CartoonSubscription.objects.filter(user=user.pk, series__series_name__contains=query)
        paginator = pagination.PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        data = CartoonSubscriptionSerializerDetailed(result_page, many=True).data
        return paginator.get_paginated_response(data)

### Adds a cartoon subscription to a user
class AddUserSubscription(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartoonSubscriptionSerializer
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        user = self.request.user
        request.data['user'] = user.pk
        serializer = CartoonSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

### Removes a user subscription
class RemoveUserSubscription(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartoonSubscriptionSerializer
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        user = self.request.user
        request.data['user'] = user.pk
        try:
            instance = CartoonSubscription.objects.filter(user=user.pk, series=request.data['series']).first()
            if instance:
                instance.delete()
                return Response({'status': 'Successfully unsubscribed'})
            else:
                return Response({'series': [
                    'Cannot unsubscribe from a cartoon that has not been subscribed to.'
                ]}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'series': [
                'This is a required field'
            ]}, status=status.HTTP_400_BAD_REQUEST)