from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

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