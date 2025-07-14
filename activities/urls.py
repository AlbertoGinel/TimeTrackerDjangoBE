# activities/urls.py
from django.urls import path
from .views import ActivityListAPIView, ActivityDetailAPIView

app_name = 'activities'

urlpatterns = [
    path('', ActivityListAPIView.as_view(), name='activity-list'),
    path('<int:pk>/', ActivityListAPIView.as_view(), name='activity-list-filtered'),  # Same view handles both
    path('<int:pk>/detail/', ActivityDetailAPIView.as_view(), name='activity-detail'),  # Keep detail view
]