from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from zoneinfo import ZoneInfo
from datetime import timedelta, datetime, time
import zoneinfo
from django.utils.functional import cached_property

User = get_user_model()

class Day(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='days'
    )
    
    # Core temporal fields
    date = models.DateField(db_index=True)  # The actual date (YYYY-MM-DD)
    timezone = models.CharField(
        max_length=50,
        default='UTC',
        choices=[(tz, tz) for tz in sorted(zoneinfo.available_timezones())]
    )
    
    # Start and end timestamps (in UTC)
    start_utc = models.DateTimeField()
    end_utc = models.DateTimeField()

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['date']
        verbose_name = "Day"
        verbose_name_plural = "Days"
    
    def __str__(self):
        return f"{self.date} ({self.user.username})"
    
    def save(self, *args, **kwargs):
        """Calculate start and end timestamps in UTC from the local date and timezone"""
        tz = ZoneInfo(self.timezone)
        local_date = self.date
        
        # Create datetime objects in the specified timezone
        local_start = datetime.combine(local_date, time.min).replace(tzinfo=tz)
        local_end = datetime.combine(local_date, time.max).replace(tzinfo=tz)
        
        # Convert to UTC
        self.start_utc = local_start.astimezone(ZoneInfo("UTC"))
        self.end_utc = local_end.astimezone(ZoneInfo("UTC"))
        
        super().save(*args, **kwargs)
    
    @property
    def week_number(self) -> int:
        """ISO week number (1-53)"""
        return self.date.isocalendar()[1]
    
    @property
    def month(self) -> int:
        """Month as integer (1-12)"""
        return self.date.month
    
    @property
    def year(self) -> int:
        """Year as integer"""
        return self.date.year
    
    @property
    def day_of_month(self) -> int:
        """Day of month (1-31)"""
        return self.date.day
    
    @property
    def day_of_week(self) -> int:
        """Day of week (1-7, Monday=1)"""
        return self.date.isoweekday()
    
    @property
    def local_start(self) -> datetime:
        """Returns start time in the day's timezone"""
        return self.start_utc.astimezone(ZoneInfo(self.timezone))
    
    @property
    def local_end(self) -> datetime:
        """Returns end time in the day's timezone"""
        return self.end_utc.astimezone(ZoneInfo(self.timezone))
    
    @classmethod
    def ensure_year_ahead(cls, user: User) -> None:
        """
        Ensures the user has days created for a year in advance.
        Uses bulk_create for better performance with many records.
        """
        today = timezone.now().date()
        one_year_later = today + timedelta(days=365)
        
        # Get existing dates for this user
        existing_dates = set(
            cls.objects.filter(user=user, date__gte=today)
            .values_list('date', flat=True)
        )
        
        # Prepare new days to create
        new_days = []
        current_date = today
        
        while current_date <= one_year_later:
            if current_date not in existing_dates:
                new_day = cls(
                    user=user,
                    date=current_date,
                    timezone=user.userTimezone
                )
                # We need to save to generate UTC times
                new_day.save()
                new_days.append(new_day)
            current_date += timedelta(days=1)

class AbstractScore(models.Model):
    day = models.ForeignKey(
        Day,
        on_delete=models.CASCADE,
        related_name='%(class)s_scores'
    )
    points = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0
    )
    
    class Meta:
        abstract = True
        ordering = ['-points']
    
    @property
    def icon(self):
        """Must be implemented by child classes"""
        raise ImproperlyConfigured(f"{self.__class__.__name__} must implement icon property")
    
    @property
    def color(self):
        """Must be implemented by child classes"""
        raise ImproperlyConfigured(f"{self.__class__.__name__} must implement color property")
    
    @property
    def name(self):
        """Must be implemented by child classes"""
        raise ImproperlyConfigured(f"{self.__class__.__name__} must implement name property")
    
    def __str__(self):
        return f"{self.name}: {self.points} points ({self.day.date})"

class ActivityScore(AbstractScore):
    activity = models.ForeignKey(
        'activities.Activity',
        on_delete=models.CASCADE,
        related_name='scores'
    )
    
    class Meta(AbstractScore.Meta):
        unique_together = ('day', 'activity')
    
    @cached_property
    def icon(self):
        return self.activity.icon
    
    @cached_property
    def color(self):
        return self.activity.color
    
    @cached_property
    def name(self):
        return self.activity.name