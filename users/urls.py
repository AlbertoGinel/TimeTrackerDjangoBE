from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from .serializers import UserListSerializer
from .views import AdminUserListView  # Import your view

User = get_user_model()

urlpatterns = [
    path('adminlist/', AdminUserListView.as_view(), name='admin-user-list'),
]