from django.urls import path
from .views import StampListCreateAPIView, StampDetailAPIView, UserIntervalsAPIView

app_name = 'stamps'

urlpatterns = [
    path('', StampListCreateAPIView.as_view(), name='stamp-list-create'),
    path('<uuid:pk>/', StampDetailAPIView.as_view(), name='stamp-detail'),
    path('intervals/', UserIntervalsAPIView.as_view(), name='user-intervals'),
]