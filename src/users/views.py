from rest_framework.views import APIView

from .serializers import  UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

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