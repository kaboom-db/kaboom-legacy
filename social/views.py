from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ThoughtSerializer, ThoughtSerializerDetailed, CommentSerializer, CommentSerializerDetailed
from django_filters import rest_framework as filters
from .filters import ThoughtFilter
from .models import Thought, Comment
from rest_framework import pagination
from rest_framework.response import Response

# Create your views here.
class ThoughtView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ThoughtFilter
    http_method_names = ['get', 'post', 'patch']

    def list(self, request):
        queryset = Thought.objects.filter(user__userdata__private=False).order_by('-date_created')
        queryset = self.filter_queryset(queryset=queryset)
        paginator = pagination.PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = ThoughtSerializerDetailed(instance=result_page, many=True)
        return paginator.get_paginated_response(data=serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            thought = Thought.objects.get(pk=pk)
            print(thought.user)
            print(self.request.user)
            if thought.user.userdata.private == False or thought.user == self.request.user:
                serializer = ThoughtSerializerDetailed(instance=thought)
                return Response(serializer.data)
            else:
                return Response({'error': 'You are not authorised to view this thought.'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'error': 'Thought with ID does not exist'}, status=status.HTTP_404_NOT_FOUND)