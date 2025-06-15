from django.urls import path
from .views import StampListCreateAPIView, StampDetailAPIView

app_name = 'stamps'

urlpatterns = [
    path('', StampListCreateAPIView.as_view(), name='stamp-list-create'),
    path('<int:pk>/', StampDetailAPIView.as_view(), name='stamp-detail'),
]