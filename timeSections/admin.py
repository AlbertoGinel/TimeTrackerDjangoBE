from django.contrib import admin
from .models import Stamp

@admin.register(Stamp)
class StampAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity', 'type', 'timestamp')
    list_filter = ('type', 'timestamp')
    search_fields = ('user__username', 'activity__name')
    date_hierarchy = 'timestamp'