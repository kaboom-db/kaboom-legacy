from rest_framework.views import APIView
from .serializers import ComicSubscriptionSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import ComicSubscription
from rest_framework import status
from rest_framework import pagination

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

class GetUserSubscriptions(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ComicSubscriptionSerializer
    http_method_names = ['get']
    
    def get(self, request):
        user = self.request.user
        queryset = ComicSubscription.objects.filter(user=user.pk)
        paginator = pagination.PageNumberPagination()
        paginator.display_page_controls = True
        print(paginator.display_page_controls)
        result_page = paginator.paginate_queryset(queryset, request)
        data = ComicSubscriptionSerializer(result_page, many=True).data
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
                return Response({'status': 'Cannot unsubscribe from a comic that has not been subscribed to.'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'series': 'This is a required field'}, status=status.HTTP_400_BAD_REQUEST)