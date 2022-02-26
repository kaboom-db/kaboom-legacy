from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ThoughtSerializer, ThoughtSerializerDetailed, CommentSerializer, CommentSerializerDetailed
from django_filters import rest_framework as filters
from .filters import ThoughtFilter, CommentFilter
from .models import Thought, Comment
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.views import APIView

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
    
    def create(self, request):
        user = self.request.user
        request.data['user'] = user.id
        serializer = ThoughtSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None):
        user = self.request.user
        try:
            thought = Thought.objects.get(pk=pk)
            # Check if the user is authorised to edit this thought
            if user == thought.user:
                request.data['user'] = thought.user.id
                serializer = ThoughtSerializer(instance=thought, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.update(instance=thought, validated_data=serializer.validated_data)
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'You are not authorised to edit this thought'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'error': 'Thought with ID does not exist'}, status=status.HTTP_404_NOT_FOUND)

class CommentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CommentFilter
    http_method_names = ['get', 'post', 'patch']

    def get(self, request, thought_id):
        try:
            thought = Thought.objects.get(id=thought_id)
            # Get all comments from that thought
            comments = Comment.objects.filter(thought=thought)
            paginator = pagination.PageNumberPagination()
            result_page = paginator.paginate_queryset(comments, request)
            serializer = CommentSerializerDetailed(instance=result_page, many=True)
            return paginator.get_paginated_response(data=serializer.data)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, thought_id):
        user = self.request.user
        try:
            thought = Thought.objects.get(id=thought_id)
            request.data['thought'] = thought.id
            request.data['user'] = user.id
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SpecificCommentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch']

    def get(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
            serializer = CommentSerializerDetailed(instance=comment)
            return Response(serializer.data)
        except:
            return Response({'error': 'Comment with ID does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, comment_id):
        user = self.request.user
        try:
            comment = Comment.objects.get(id=comment_id)
            if comment.user == user:
                request.data['thought'] = comment.thought.id
                request.data['user'] = comment.user.id
                serializer = CommentSerializer(instance=comment, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.update(instance=comment, validated_data=serializer.validated_data)
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'You are not authorised to edit this comment'}, status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# // TODO(#7): Write user feeds
# //    User feeds should have the ability to take a type as part of the query param
# //    For example; type=comics which would show the comics read by the user followings
