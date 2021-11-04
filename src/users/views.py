from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response

class CreateUser(APIView):
    def post(self, request):
        post_data = request.data
        print(post_data)
        serializer = UserSerializer(data=post_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                serializer.data
            })
        return Response({
            serializer.errors
        })