from django.contrib import admin
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'color', 'points_per_hour', 'created_at')
    list_select_related = ('user',)  # Optimizes DB queries
    search_fields = ('name', 'user__username', 'user__email')
    list_filter = ('user', 'color', 'created_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'color', 'icon')
        }),
        ('Points Settings', {
            'fields': ('points_per_hour', 'seconds_free'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )