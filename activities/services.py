#/activites/services.py
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from api.core.permissions import AccessValidator
from .models import Activity
from .serializers import ActivitySerializer

User = get_user_model()

class ActivityService:

    @staticmethod
    def get_user_activities(user_id, requesting_user):
        """Retrieve activities for a user with permission check"""
        AccessValidator.validate_user_access(requesting_user, user_id)
        return Activity.objects.filter(user_id=user_id).select_related('user')

    @staticmethod
    def create_activity(data, requesting_user):
        """Create new activity with permission validation"""
        user_id = data.get('user', requesting_user.id)
        AccessValidator.validate_user_access(requesting_user, user_id)

        serializer = ActivitySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    @staticmethod
    def update_activity(pk, data, requesting_user):
        """Update existing activity"""
        activity = Activity.objects.get(pk=pk)
        AccessValidator.validate_user_access(requesting_user, activity.user.id)

        # Prevent non-staff from changing ownership
        if 'user' in data and int(data['user']) != activity.user.id:
            if not requesting_user.is_staff:
                raise PermissionDenied("Cannot transfer activity ownership")

        serializer = ActivitySerializer(activity, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    @staticmethod
    def delete_activity(pk, requesting_user):
        """Delete activity with permission check"""
        activity = Activity.objects.get(pk=pk)
        AccessValidator.validate_user_access(requesting_user, activity.user.id)
        activity.delete()



