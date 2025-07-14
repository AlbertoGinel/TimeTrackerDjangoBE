from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from .serializers import UserListSerializer

User = get_user_model()

class AdminUserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        if not request.user.is_staff:
            return Response({"error": "Forbidden"}, status=403)

        # Superusers see all users, regular admins see only non-staff
        if request.user.is_superuser:
            users = User.objects.all()
        else:
            users = User.objects.filter(is_staff=False)

        users = users.order_by('last_name', 'first_name')
        serializer = UserListSerializer(users, many=True, context={'request': request})
        return Response({
            'count': users.count(),
            'results': serializer.data
        })
