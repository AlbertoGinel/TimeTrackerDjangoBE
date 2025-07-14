from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DayViewSet

router = DefaultRouter()
router.register(r'days', DayViewSet, basename='day')

urlpatterns = [
    path('', include(router.urls)),
]