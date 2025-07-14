# core/permissions.py
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied

User = get_user_model()

class AccessValidator:
    @staticmethod
    def validate_user_access(requesting_user, target_user_id, message=None):
        """
        Universal user access validator
        Args:
            requesting_user: User making the request
            target_user_id: ID of user being accessed
            message: Custom error message (optional)
        """
        if int(target_user_id) != requesting_user.id:
            if not User.objects.filter(
                id=requesting_user.id,
                is_staff=True
            ).exists():
                raise PermissionDenied(
                    message or "You don't have permission to access this resource"
                )
        return True