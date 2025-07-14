# api/urls.py
from django.urls import path
from api.views.views import UserDashboardAPIView

urlpatterns = [
    path('users/<int:user_id>/dashboard/', UserDashboardAPIView.as_view()),
]