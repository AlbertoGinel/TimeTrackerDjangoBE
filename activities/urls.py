# activities/urls.py
from django.urls import path
from .views import ActivityListAPIView, ActivityDetailAPIView

app_name = 'activities'

urlpatterns = [
    # API Endpoints only
    path('', ActivityListAPIView.as_view(), name='activity-list'),
    path('<uuid:pk>/', ActivityDetailAPIView.as_view(), name='activity-detail'),
]