#/main url
from . import views
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenObtainPairView
)
from .views import TokenObtainPairView

urlpatterns = [
    # Admin
    ## path('admin/', admin.site.urls),


    # Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # New unified API endpoints
    path('api/combi/', include('api.urls.urls')),

    # Users
    path('api/users/', include('users.urls')), #used!!

    # Activities
    path('api/activities/', include('activities.urls')),

    # Stamps
    path('api/timeSections/', include('timeSections.urls')),


    # Keep old endpoints for now (consider deprecating later)
    path('api/legacy/activities/', include('activities.urls')),
    path('api/legacy/days/', include('days.urls')),
]

