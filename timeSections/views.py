from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated


from timeSections.models import Stamp
from .services import StampService, IntervalService
from .serializers import StampSerializer, IntervalSerializer
from api.permissions import IsAdminOrOwner

class UserStampListAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    """GET /users/<user_id>/stamps/"""
    def get(self, request, user_id):
        try:
            request_data = {'user': user_id}
            stamps = StampService.get_user_stamps(request_data, request.user)
            serializer = StampSerializer(stamps, many=True)
            return Response(serializer.data)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied:
            raise PermissionDenied("You don't have permission to access these stamps")


class StampCreateAPIView(APIView):
    """POST /stamps/"""
    def post(self, request):

        try:
            # Service now returns Stamp instance
            stamp = StampService.create_stamp(request.data, request.user)
            serializer = StampSerializer(stamp)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied:
            raise PermissionDenied("You don't have permission to create stamps for this user")

class StampDetailAPIView(APIView):
    """GET/PUT/DELETE /stamps/<pk>/"""
    def get(self, request, pk):
        try:
            # Service returns single Stamp instance
            stamp = StampService.get_stamp_by_id(pk, request.user)
            serializer = StampSerializer(stamp)
            return Response(serializer.data)
        except Stamp.DoesNotExist:
            raise NotFound("Stamp not found")
        except PermissionDenied:
            raise PermissionDenied("You don't own this stamp")

    def put(self, request, pk):

        try:
            # Service returns updated Stamp instance
            stamp = StampService.update_stamp(pk, request.data, request.user)
            serializer = StampSerializer(stamp)
            return Response(serializer.data)
        except Stamp.DoesNotExist:
            raise NotFound("Stamp not found")
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied:
            raise PermissionDenied("You can't modify this stamp")

    def delete(self, request, pk):
        try:
            StampService.delete_stamp(pk, request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Stamp.DoesNotExist:
            raise NotFound("Stamp not found")
        except PermissionDenied:
            raise PermissionDenied("You can't delete this stamp")

class UserIntervalsAPIView(APIView):
    """GET /users/<user_id>/intervals/"""
    def get(self, request, user_id):
        try:
            request_data = {'user': user_id}
            # Service returns list of Interval objects
            intervals = IntervalService.get_user_intervals(request_data, request.user)
            serializer = IntervalSerializer(intervals, many=True)
            return Response(serializer.data)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied:
            raise PermissionDenied("You don't have permission to view these intervals")