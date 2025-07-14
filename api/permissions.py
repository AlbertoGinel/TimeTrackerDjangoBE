# permissions.py
from rest_framework.permissions import BasePermission

class IsAdminOrOwner(BasePermission):
    """
    Modified for APIView compatibility
    """
    
    def has_permission(self, request, view):
        # For list views (GET requests)
        if request.method == 'GET':
            user_id = view.kwargs.get('user_id')
            return request.user.is_staff or str(request.user.id) == user_id
        return True
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user