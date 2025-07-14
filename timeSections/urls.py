from django.urls import path
from .views import (
    UserStampListAPIView,  # For /users/<user_id>/stamps/
    StampDetailAPIView,    # For /stamps/<pk>/
    UserIntervalsAPIView,   # For /users/<user_id>/intervals/
    StampCreateAPIView
)

urlpatterns = [
    # Get all stamps for a specific user
    path('users/<int:user_id>/stamps/', UserStampListAPIView.as_view(), name='user-stamps'),
    
    # Single stamp operations (GET/PUT/DELETE)
    path('stamps/<uuid:pk>/', StampDetailAPIView.as_view(), name='stamp-detail'),
    
    # Get intervals for a specific user
    path('users/<int:user_id>/intervals/', UserIntervalsAPIView.as_view(), name='user-intervals'),
    
    # Create new stamp (POST-only endpoint)
    path('stamps/', StampCreateAPIView.as_view(), name='stamp-create'),
]