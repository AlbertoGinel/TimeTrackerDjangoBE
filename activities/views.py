# activities/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, NotFound
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Activity
from .serializers import ActivitySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import ActivityService

class ActivityListAPIView(APIView):

    permission_classes = [IsAuthenticated]

class ActivityListAPIView(APIView):
    def get(self, request, pk=None):  # pk is now optional
        # If pk is provided (e.g., /api/activities/3/), use it as user_id
        target_user_id = pk if pk is not None else request.user.id
        activities = ActivityService.get_user_activities(target_user_id, request.user)
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = ActivityService.create_activity(request.data, request.user)
        return Response(data, status=status.HTTP_201_CREATED)

class ActivityDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        activity = ActivityService.get_activity_detail(pk, request.user)
        serializer = ActivitySerializer(activity)
        return Response(serializer.data)

    def put(self, request, pk):
        data = ActivityService.update_activity(pk, request.data, request.user)
        return Response(data)

    def delete(self, request, pk):
        ActivityService.delete_activity(pk, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)