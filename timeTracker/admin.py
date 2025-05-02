from django.contrib import admin
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'color', 'points_per_hour', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('user', 'color')