from rest_framework import viewsets, permissions, filters
from .models import Day
from .serializers import DaySerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta

class DayViewSet(viewsets.ModelViewSet):
    queryset = Day.objects.all()
    serializer_class = DaySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'date', 'timezone']
    ordering_fields = ['date', 'start_utc']
    ordering = ['-date']  # Default ordering
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Optionally restricts the returned days to a given user,
        by filtering against a `user` query parameter in the URL.
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        # Non-admin users can only see their own days
        if not user.is_staff:
            queryset = queryset.filter(user=user)
        
        # Filter by date range if provided
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
            
        return queryset