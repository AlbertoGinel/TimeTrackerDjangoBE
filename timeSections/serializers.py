from rest_framework import serializers
from .models import Stamp
from activities.models import Activity
from activities.serializers import ActivitySerializer

class StampSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer(read_only=True)
    activity_id = serializers.PrimaryKeyRelatedField(
        queryset=Activity.objects.all(),
        source='activity',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Stamp
        fields = ['id', 'type', 'timestamp', 'activity', 'activity_id', 'user']
        read_only_fields = ['id', 'timestamp', 'user']
        extra_kwargs = {
            'id': {
                'required': False  # Ensure DRF doesn't require ID in input
            }
        }

    def validate_activity(self, value):
        if value is not None and value.user != self.context['request'].user:
            raise serializers.ValidationError(
                "Activity does not belong to the current user."
            )
        return value

    def validate(self, data):
        if data.get('type') == 'start' and data.get('activity') is None:
            raise serializers.ValidationError(
                {"activity_id": "Activity is required for start stamps."}
            )
        return data

    def create(self, validated_data):
        # Set the user automatically from request
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)



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
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    activity = ActivitySerializer(read_only=True)
    fromDate = serializers.DateTimeField(source='opening_stamp.timestamp', read_only=True)
    toDate = serializers.DateTimeField(source='closing_stamp.timestamp', read_only=True, allow_null=True)
    duration = serializers.SerializerMethodField()
    is_open = serializers.SerializerMethodField()

    def get_duration(self, obj):
        return obj.duration

    def get_is_open(self, obj):
        return obj.closing_stamp is None

    def validate(self, data):
        """
        Validate that:
        1. Opening stamp is a START type
        2. Both stamps belong to the same user
        """
        opening_stamp = data.get('opening_stamp')
        closing_stamp = data.get('closing_stamp')

        if opening_stamp.type != Stamp.StampType.START:
            raise serializers.ValidationError({
                'opening_stamp': "Opening stamp must be of type START"
            })

        if closing_stamp and opening_stamp.user != closing_stamp.user:
            raise serializers.ValidationError({
                'closing_stamp': "Stamps must belong to the same user"
            })

        return data

    def create(self, validated_data):
        """
        Normally you wouldn't create intervals directly (they're derived from stamps),
        but if needed, this would create an interval record.
        """
        return Interval(
            opening_stamp=validated_data['opening_stamp'],
            closing_stamp=validated_data.get('closing_stamp')
        )