from django.utils import timezone
from api.core.permissions import AccessValidator
from rest_framework.exceptions import ValidationError
from .models import Stamp
from .serializers import StampSerializer
from django.contrib.auth import get_user_model
from .utils import get_user_intervals

User = get_user_model()

class StampService:
    @staticmethod
    def get_user_stamps(request_data, requesting_user):
        """Get stamps for specified user"""
        user_id = request_data.get('user')
        if not user_id:
            raise ValidationError({"user": "This field is required"})

        # Validate access rights
        AccessValidator.validate_user_access(requesting_user, user_id)

        # Return data for target user
        return Stamp.objects.filter(user_id=user_id)

    @staticmethod
    def get_stamp_by_id(pk, requesting_user):
        """Get single stamp by ID with ownership validation"""
        stamp = Stamp.objects.get(pk=pk)
        # Validate access rights - will raise PermissionDenied if invalid
        AccessValidator.validate_user_access(requesting_user, stamp.user.id)
        return stamp

    @staticmethod
    def create_stamp(request_data, requesting_user):
        """Create stamp for target user"""
        user_id = request_data.get('user')
        if not user_id:
            raise ValidationError({"user": "This field is required"})

        # Strict permission check
        AccessValidator.validate_user_access(requesting_user, user_id)

        # Prepare data - ensure admin can't be accidentally assigned
        create_data = {
            **request_data,
            'timestamp': request_data.get('timestamp', timezone.now()),
            'user': user_id  # Force use of validated user_id
        }

        # Create for target user
        serializer = StampSerializer(
            data=create_data,
            context={'request': requesting_user}  # For any serializer validation
        )
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    def update_stamp(pk, request_data, requesting_user):

        """Update existing stamp with ownership checks"""
        stamp = Stamp.objects.get(pk=pk)

        # Original ownership check
        AccessValidator.validate_user_access(requesting_user, stamp.user.id)

        # If changing owner, verify admin rights
        if 'user' in request_data and str(request_data['user']) != str(stamp.user.id):
            AccessValidator.validate_staff_access(requesting_user)

        serializer = StampSerializer(
            stamp,
            data=request_data,
            context={'request': requesting_user},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    def delete_stamp(pk, requesting_user):
        """Delete stamp after ownership validation"""
        stamp = Stamp.objects.get(pk=pk)
        AccessValidator.validate_user_access(requesting_user, stamp.user.id)
        stamp.delete()

class IntervalService:
    @staticmethod
    def get_user_intervals(request_data, requesting_user):
        """Get intervals for specified user"""
        user_id = request_data.get('user')
        if not user_id:
            raise ValidationError({"user": "This field is required"})

        # Validate access
        AccessValidator.validate_user_access(requesting_user, user_id)

        # Get intervals for target user
        target_user = User.objects.get(id=user_id)
        intervals = get_user_intervals(target_user)
        return sorted(intervals, key=lambda x: x.fromDate, reverse=True)