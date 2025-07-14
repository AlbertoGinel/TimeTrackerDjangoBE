from rest_framework import serializers
from .models import Day
from django.contrib.auth import get_user_model

User = get_user_model()

class DaySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    # Read-only properties
    week_number = serializers.IntegerField(read_only=True)
    month = serializers.IntegerField(read_only=True)
    year = serializers.IntegerField(read_only=True)
    day_of_month = serializers.IntegerField(read_only=True)
    day_of_week = serializers.IntegerField(read_only=True)
    local_start = serializers.DateTimeField(read_only=True)
    local_end = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Day
        fields = [
            'id', 'user', 'date', 'timezone', 'start_utc', 'end_utc',
            'week_number', 'month', 'year', 'day_of_month', 'day_of_week',
            'local_start', 'local_end'
        ]
        read_only_fields = ['start_utc', 'end_utc']