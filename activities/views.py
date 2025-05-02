from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Activity
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ActivitySerializer
from rest_framework.permissions import IsAuthenticated

# Template Views (for HTML rendering)
class ActivityListView(LoginRequiredMixin, ListView):
    model = Activity
    template_name = 'activities/activity_list.html'
    context_object_name = 'activities'

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)

class ActivityDetailView(LoginRequiredMixin, DetailView):
    model = Activity
    template_name = 'activities/activity_detail.html'
    context_object_name = 'activity'

class ActivityCreateView(LoginRequiredMixin, CreateView):
    model = Activity
    fields = ['name', 'color', 'icon', 'points_per_hour', 'seconds_free']
    template_name = 'activities/activity_form.html'
    success_url = reverse_lazy('activities:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    model = Activity
    fields = ['name', 'color', 'icon', 'points_per_hour', 'seconds_free']
    template_name = 'activities/activity_form.html'
    success_url = reverse_lazy('activities:list')

class ActivityDeleteView(LoginRequiredMixin, DeleteView):
    model = Activity
    template_name = 'activities/activity_confirm_delete.html'
    success_url = reverse_lazy('activities:list')

# API Views (for JSON endpoints)
class ActivityListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        activities = Activity.objects.filter(user=request.user)
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivityDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Activity.objects.get(pk=pk, user=self.request.user)
        except Activity.DoesNotExist:
            return None
    
    def get(self, request, pk):
        activity = self.get_object(pk)
        if activity:
            serializer = ActivitySerializer(activity)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        activity = self.get_object(pk)
        if activity:
            serializer = ActivitySerializer(activity, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        activity = self.get_object(pk)
        if activity:
            activity.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)