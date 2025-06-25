from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Stamp
from .serializers import StampSerializer
from .serializers import IntervalSerializer
#from activities.models import Activity
from .utils import get_user_intervals

class StampListCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        stamps = Stamp.objects.filter(user=request.user)
        serializer = StampSerializer(stamps, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StampSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StampDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Stamp.objects.get(pk=pk, user=self.request.user)
        except Stamp.DoesNotExist:
            return None
    
    def get(self, request, pk):
        stamp = self.get_object(pk)
        if stamp:
            serializer = StampSerializer(stamp)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        stamp = self.get_object(pk)
        if not stamp:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = StampSerializer(stamp, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        stamp = self.get_object(pk)
        if stamp:
            stamp.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class UserIntervalsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Generate intervals from stamps
        intervals = get_user_intervals(request.user)
        intervals = sorted(intervals, key=lambda x: x.fromDate, reverse=True)
        # Serialize virtual Interval objects
        serializer = IntervalSerializer(intervals, many=True)
        return Response(serializer.data)