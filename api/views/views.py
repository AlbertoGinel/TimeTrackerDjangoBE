# /api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response

from activities.services import ActivityService
from activities.serializers import ActivitySerializer
# from intervals.services import IntervalService
# from users.services import UserService


class UserDashboardAPIView(APIView):
    def get(self, request, user_id):
        """
        Return a dashboard with user-related data (activities, intervals, stats, etc.)
        """
        dashboard_data = {
            # 'user': UserService.get_user_profile(user_id, request.user),
            'activities': ActivitySerializer(
                ActivityService.get_user_activities(user_id, request.user),
                many=True
            ).data,
            # 'intervals': IntervalService.get_user_intervals(user_id, request.user),
            # 'stats': {
            #     'activity_count': ActivityService.get_user_activities(
            #         user_id, request.user
            #     ).count(),
            #     # Add more stats as needed
            # }
        }

        return Response(dashboard_data)
