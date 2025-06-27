# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from zoneinfo import ZoneInfo
from zoneinfo import available_timezones  # All IANA timezones

class CustomUser(AbstractUser):
    # Auto-set on user creation
    startUser = models.DateTimeField(default=timezone.now)

    # Timezone field (dropdown of all IANA timezones)
    timezone = models.CharField(
        max_length=50,
        choices=[(tz, tz) for tz in sorted(available_timezones())],
        default="UTC",
    )

    def __str__(self):
        return self.username