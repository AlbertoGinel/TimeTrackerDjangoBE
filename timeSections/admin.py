from django.contrib import admin
from .models import Stamp

@admin.register(Stamp)
class StampAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'activity', 'type', 'timestamp')  # Added 'id'
    list_display_links = ('id', 'user')  # Make both ID and user clickable
    list_filter = ('type', 'timestamp')
    search_fields = ('user__username', 'activity__name', 'id')  # Added 'id' to search
    date_hierarchy = 'timestamp'
    readonly_fields = ('id',)  # Make UUID non-editable
    ordering = ('-timestamp',)  # Explicit ordering to match model Meta

    def get_readonly_fields(self, request, obj=None):
        # Make ID read-only when editing existing objects
        if obj:  # Editing an existing object
            return self.readonly_fields + ('timestamp',)
        return self.readonly_fields