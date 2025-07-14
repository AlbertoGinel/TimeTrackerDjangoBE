from rest_framework_simplejwt.views import TokenObtainPairView as BaseTokenObtainPairView
from .serializers import TokenObtainPairSerializer

class TokenObtainPairView(BaseTokenObtainPairView):
    """Uses our custom serializer instead of default"""
    serializer_class = TokenObtainPairSerializer