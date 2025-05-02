from django.urls import path
from .views import (
    ActivityListView,
    ActivityDetailView,
    ActivityCreateView,
    ActivityUpdateView,
    ActivityDeleteView,
    ActivityListAPIView,
    ActivityDetailAPIView
)

app_name = 'activities'

urlpatterns = [
    # Web Interface URLs
    path('', ActivityListView.as_view(), name='list'),
    path('new/', ActivityCreateView.as_view(), name='create'),
    path('<uuid:pk>/', ActivityDetailView.as_view(), name='detail'),
    path('<uuid:pk>/edit/', ActivityUpdateView.as_view(), name='update'),
    path('<uuid:pk>/delete/', ActivityDeleteView.as_view(), name='delete'),

    # API Endpoints
    path('api/', ActivityListAPIView.as_view(), name='api-list'),
    path('api/<uuid:pk>/', ActivityDetailAPIView.as_view(), name='api-detail'),
]