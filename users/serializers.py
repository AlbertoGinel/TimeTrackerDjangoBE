from rest_framework import serializers

from .models import CustomUser

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
    "id",
    "last_login",
    "username",
    "first_name",
    "last_name",
    "email",
    "is_staff",
    "is_active",
    "date_joined",
    "userTimezone"
]

    def to_representation(self, instance):
        """Remove sensitive fields for non-superusers"""
        data = super().to_representation(instance)
        if not self.context['request'].user.is_superuser:
            data.pop('is_staff', None)
        return data
