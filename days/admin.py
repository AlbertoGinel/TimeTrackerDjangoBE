from django.contrib import admin
from django.utils.html import format_html
from .models import Day, ActivityScore

@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ('formatted_date', 'formatted_user', 'timezone', 'formatted_start_utc', 'formatted_end_utc', 'score_count')
    list_filter = ('timezone', 'user', 'date')
    search_fields = ('user__username', 'date')
    date_hierarchy = 'date'
    fieldsets = (
        (None, {
            'fields': ('user', 'date', 'timezone')
        }),
        ('Timestamps', {
            'fields': ('start_utc', 'end_utc'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('start_utc', 'end_utc')
        return self.readonly_fields
    
    # Custom display methods
    def formatted_date(self, obj):
        return obj.date.strftime('%Y/%m/%d')
    formatted_date.short_description = 'Date'
    formatted_date.admin_order_field = 'date'
    
    def formatted_user(self, obj):
        return f"{obj.user} ({obj.timezone})"
    formatted_user.short_description = 'User'
    formatted_user.admin_order_field = 'user'
    
    def formatted_start_utc(self, obj):
        return obj.start_utc.isoformat() if obj.start_utc else ''
    formatted_start_utc.short_description = 'Start UTC'
    formatted_start_utc.admin_order_field = 'start_utc'
    
    def formatted_end_utc(self, obj):
        return obj.end_utc.isoformat() if obj.end_utc else ''
    formatted_end_utc.short_description = 'End UTC'
    formatted_end_utc.admin_order_field = 'end_utc'
    
    def score_count(self, obj):
        # Count all types of scores for this day
        count = 0
        for related in ['activityscore_scores']:
            count += getattr(obj, related).count()
        return count
    score_count.short_description = 'Total Scores'

# Common admin class for all score types
class BaseScoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'colored_icon', 'day_link', 'points', 'formatted_date')
    list_filter = ('day__user', 'day__date')
    search_fields = ('name', 'day__date', 'day__user__username')
    readonly_fields = ('colored_icon_display',)
    fieldsets = (
        (None, {
            'fields': ('day', 'name', 'icon', 'color', 'points')
        }),
        ('Display', {
            'fields': ('colored_icon_display',),
            'classes': ('collapse',)
        }),
    )
    
    def formatted_date(self, obj):
        return obj.day.date.strftime('%Y/%m/%d')
    formatted_date.short_description = 'Date'
    formatted_date.admin_order_field = 'day__date'
    
    def day_link(self, obj):
        url = f"/admin/yourapp/day/{obj.day.id}/change/"
        return format_html('<a href="{}">{}</a>', url, obj.day)
    day_link.short_description = 'Day'
    day_link.admin_order_field = 'day'
    
    def colored_icon(self, obj):
        return format_html(
            '<span style="color: {};">{}</span>',
            obj.color,
            obj.icon
        )
    colored_icon.short_description = 'Icon'
    
    def colored_icon_display(self, obj):
        return self.colored_icon(obj)
    colored_icon_display.short_description = 'Icon Preview'

# Register concrete score models with the common admin class
@admin.register(ActivityScore)
class ActivityScoreAdmin(BaseScoreAdmin):
    fieldsets = BaseScoreAdmin.fieldsets + (
        ('Activity Specific', {
            'fields': ('activity',),
            'classes': ('collapse',)
        }),
    )
    list_display = BaseScoreAdmin.list_display + ('activity',)