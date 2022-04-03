from .models import Character, Format, Issue, Comic, Publisher, Staff, StaffPositions
from rest_framework import status, viewsets
from .serializers import FormatSerializer, IssueSerializer, PublisherSerializer, CharacterSerializer, SeriesSerializer, StaffPositionsSerializer, StaffSerializer
from django.db.models import Q
from rest_framework import pagination
from rest_framework.authentication import TokenAuthentication
from django_filters import rest_framework as filters
from .comics_filters import FormatFilter, IssuesFilter, PublishersFilters, StaffFilter, SeriesFilter, StaffPositionsFilter
from cartoons.views import AllowGetAuthentication
from rest_framework.response import Response

class PublisherView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowGetAuthentication]
    serializer_class = PublisherSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PublishersFilters
    http_method_names = ['get', 'post', 'patch']

    def list(self, request):
        queryset = Publisher.objects.all().order_by('name')
        queryset = self.filter_queryset(queryset=queryset)
        paginator = pagination.PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = PublisherSerializer(instance=result_page, many=True)
        return paginator.get_paginated_response(data=serializer.data)

    def create(self, request):
        if request.data:
            serializer = PublisherSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Request body must not be empty'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            publisher = Publisher.objects.get(pk=pk)
            serializer = PublisherSerializer(instance=publisher)
            return Response(serializer.data)
        except:
            return Response({'error': 'Publisher with ID does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            publisher = Publisher.objects.get(pk=pk)
            if request.data:
                serializer = PublisherSerializer(instance=publisher, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.update(instance=publisher, validated_data=serializer.validated_data)
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Request body must not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class StaffView(viewsets.ReadOnlyModelViewSet):
    serializer_class = StaffSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StaffFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowGetAuthentication]
    http_method_names = ['get', 'post', 'patch']

    def list(self, request):
        queryset = Staff.objects.all().order_by('name')
        queryset = self.filter_queryset(queryset=queryset)
        paginator = pagination.PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = StaffSerializer(instance=result_page, many=True)
        return paginator.get_paginated_response(data=serializer.data)

    def create(self, request):
        if request.data:
            serializer = StaffSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Request body must not be empty'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            staff = Staff.objects.get(pk=pk)
            serializer = StaffSerializer(instance=staff)
            return Response(serializer.data)
        except:
            return Response({'error': 'Staff with ID does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            staff = Staff.objects.get(pk=pk)
            if request.data:
                serializer = StaffSerializer(instance=staff, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.update(instance=staff, validated_data=serializer.validated_data)
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Request body must not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class IssueView(viewsets.ReadOnlyModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IssuesFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowGetAuthentication]
    http_method_names = ['get', 'post', 'patch']

    def list(self, request):
        queryset = Issue.objects.all().order_by('issue_number_absolute')
        queryset = self.filter_queryset(queryset=queryset)
        paginator = pagination.PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = IssueSerializer(instance=result_page, many=True)
        return paginator.get_paginated_response(data=serializer.data)

    def create(self, request):
        try:
            if request.data:
                serializer = IssueSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Request body must not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            issue = Issue.objects.get(pk=pk)
            serializer = IssueSerializer(instance=issue)
            return Response(serializer.data)
        except:
            return Response({'error': 'Issue with ID does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            issue = Issue.objects.get(pk=pk)
            if request.data:
                data = request.data.copy()
                data['series'] = issue.series.id
                serializer = IssueSerializer(instance=issue, data=data, partial=True)
                if serializer.is_valid():
                    serializer.update(instance=issue, validated_data=serializer.validated_data)
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Request body must not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SeriesView(viewsets.ReadOnlyModelViewSet):
    serializer_class = SeriesSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SeriesFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowGetAuthentication]
    http_method_names = ['get', 'post', 'patch']

    def list(self, request):
        queryset = Comic.objects.all().order_by('series_name')
        queryset = self.filter_queryset(queryset=queryset)
        paginator = pagination.PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = SeriesSerializer(instance=result_page, many=True)
        return paginator.get_paginated_response(data=serializer.data)

    def create(self, request):
        if request.data:
            serializer = SeriesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Request body must not be empty'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            series = Comic.objects.get(pk=pk)
            serializer = SeriesSerializer(instance=series)
            return Response(serializer.data)
        except:
            return Response({'error': 'Comic with ID does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            series = Comic.objects.get(pk=pk)
            if request.data:
                serializer = SeriesSerializer(instance=series, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.update(instance=series, validated_data=serializer.validated_data)
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Request body must not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class StaffPositionsView(viewsets.ReadOnlyModelViewSet):
    queryset = StaffPositions.objects.all()
    serializer_class = StaffPositionsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StaffPositionsFilter

class FormatsView(viewsets.ReadOnlyModelViewSet):
    queryset = Format.objects.all()
    serializer_class = FormatSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FormatFilter