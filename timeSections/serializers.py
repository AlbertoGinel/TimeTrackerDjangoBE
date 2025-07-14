from django.forms import ValidationError
from rest_framework import serializers
from .models import Interval, Stamp
from activities.models import Activity
from activities.serializers import ActivitySerializer

class StampSerializer(serializers.ModelSerializer):

    activity = serializers.PrimaryKeyRelatedField(
        queryset=Activity.objects.all(),
        pk_field=serializers.UUIDField(),
        write_only=True
    )

    # For reads: full nested representation
    activity_data = ActivitySerializer(source='activity', read_only=True)

    class Meta:
        model = Stamp
        fields = ['id', 'type', 'timestamp', 'user', 'activity', 'activity_data']

    def validate(self, data):
        """Pure data validation without business logic"""
        if data.get('type') == 'start' and not data.get('activity'):
            raise serializers.ValidationError(
                {"activity": "Required for start stamps"}
            )
        return data

    def create(self, validated_data):
        """Let views/services handle permissions, just save data"""
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class IntervalSerializer(serializers.Serializer):
    opening_stamp = serializers.PrimaryKeyRelatedField(
        queryset=Stamp.objects.all(),
        required=True
    )
    closing_stamp = serializers.PrimaryKeyRelatedField(
        queryset=Stamp.objects.all(),
        required=False,
        allow_null=True
    )

    # Read-only fields
    start = serializers.DateTimeField(source='fromDate', read_only=True)
    end = serializers.DateTimeField(source='toDate', read_only=True, allow_null=True)
    duration = serializers.DurationField(read_only=True)
    is_open = serializers.BooleanField(read_only=True)
    activity = ActivitySerializer(source='opening_stamp.activity', read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        source='opening_stamp.user', 
        read_only=True
    )

    def validate(self, data):
        opening_stamp = data['opening_stamp']
        
        if opening_stamp.type != Stamp.StampType.START:
            raise ValidationError({
                'opening_stamp': "Must be a START type stamp"
            })
            
        if (closing_stamp := data.get('closing_stamp')) and \
           (opening_stamp.user != closing_stamp.user):
            raise ValidationError({
                'closing_stamp': "Must belong to same user as opening stamp"
            })

        return data

    def create(self, validated_data):
        """For manual interval creation (if needed)"""
        return Interval(
            opening_stamp=validated_data['opening_stamp'],
            closing_stamp=validated_data.get('closing_stamp')
        )
