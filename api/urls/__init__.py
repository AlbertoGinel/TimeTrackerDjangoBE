from django.urls import path
from users.views import AdminUserListView  # Import from users app

urlpatterns = [
    path('users/', AdminUserListView.as_view(), name='admin-user-list'),
]