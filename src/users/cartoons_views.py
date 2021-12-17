from rest_framework.views import APIView

from cartoons.models import Series
from .serializers import ComicSubscriptionSerializer, ComicSubscriptionSerializerDetailed, ReadIssuesSerializer, ReadIssuesSerializerDetailed, UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import ComicSubscription, ReadIssue
from rest_framework import status
from rest_framework import pagination
from django.core.exceptions import ObjectDoesNotExist

### Gets a users cartoons subscriptions
class GetUserSubscriptions(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]