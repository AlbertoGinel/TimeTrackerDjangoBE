from rest_framework import serializers
from .models import Activity

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'name', 'color', 'icon', 'points_per_hour', 'seconds_free', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']