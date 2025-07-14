from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class TokenObtainPairSerializer(TokenObtainPairSerializer):
    """Extends default token serializer to include user data"""
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'userTimezone': user.userTimezone,
            'is_staff': user.is_staff,
            'last_login': user.last_login,
            'date_joined': user.date_joined,
            'is_active': user.is_active,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        return data
