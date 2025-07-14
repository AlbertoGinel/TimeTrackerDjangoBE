# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from zoneinfo import ZoneInfo, available_timezones
from django.core.exceptions import ValidationError


TIMEZONE_CHOICES = [(tz, tz) for tz in sorted(available_timezones())]

class CustomUser(AbstractUser):

    userTimezone = models.CharField(
        max_length=50,
        default="Etc/UTC",
        choices=TIMEZONE_CHOICES
    )

    def clean(self):
        """Ensure the timezone is valid before saving."""
        super().clean()
        try:
            ZoneInfo(self.userTimezone )  # Will raise ZoneInfoNotFoundError if invalid
        except Exception as e:
            raise ValidationError(
                {"timezone": f"Invalid timezone: {self.userTimezone }. Must be a valid IANA timezone."}
            )

    def save(self, *args, **kwargs):
        """Run full validation before saving."""
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def tzinfo(self):
        """Get the timezone as a ZoneInfo object for datetime conversions."""
        return ZoneInfo(self.userTimezone )

    def __str__(self):
        return self.username

    class Meta:
        permissions = [
            ("manage_regular_users", "Can manage non-admin users")
        ]


