
from rest_framework import serializers
from .models import Stamp
from activities.models import Activity
from activities.serializers import ActivitySerializer

class StampSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer(read_only=True)  # 👈 Full nested activity for output
    activity_id = serializers.PrimaryKeyRelatedField(  # 👈 Still allow creation with ID
        queryset=Activity.objects.all(),
        source='activity',
        write_only=True
    )

    class Meta:
        model = Stamp
        fields = ['id', 'type', 'timestamp', 'activity', 'activity_id', 'user']
        read_only_fields = ['id', 'timestamp', 'user']

    def validate_activity(self, value):
        if value.user != self.context['request'].user:
            raise serializers.ValidationError(
                "Activity does not belong to the current user."
            )
        return value
