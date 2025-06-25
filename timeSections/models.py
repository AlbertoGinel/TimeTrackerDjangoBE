from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid

User = get_user_model()

class Stamp(models.Model):
    class StampType(models.TextChoices):
        START = 'start', 'Start'
        STOP = 'stop', 'Stop'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    type = models.CharField(
        max_length=5,
        choices=StampType.choices,
        default=StampType.START
    )
    timestamp = models.DateTimeField(default=timezone.now)
    activity = models.ForeignKey(
        'activities.Activity',
        on_delete=models.CASCADE,
        related_name='stamps',
        null=True,  # Allow NULL
        blank=True  # Allow blank in forms
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='stamps'
    )

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'activity']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.type} at {self.timestamp}"

    def clean(self):
        # Only validate activity relationship if activity exists
        if self.activity and self.user != self.activity.user:
            raise ValidationError("Stamp user must match activity user.")

        # Require activity for START stamps
        if self.type == self.StampType.START and not self.activity:
            raise ValidationError("Start stamps require an activity.")



# INTERVALS


class Interval:
    # No models.Model inheritance → No DB table
    """Virtual model representing time intervals derived from stamps."""
    def __init__(self, opening_stamp, closing_stamp=None):
        self.opening_stamp = opening_stamp
        self.closing_stamp = closing_stamp
        self.user = opening_stamp.user
        self.activity = opening_stamp.activity
        self.fromDate = opening_stamp.timestamp
        self.toDate = closing_stamp.timestamp if closing_stamp else None

    @property
    def duration(self):
        """Returns timedelta (open intervals use current time)."""
        end = self.toDate or timezone.now()
        return end - self.fromDate

    @property
    def is_open(self):
        return self.closing_stamp is None

    def __str__(self):
        status = "OPEN" if self.is_open else "CLOSED"
        return f"{self.user.username} - {self.activity.name} ({status}) {self.fromDate} → {self.toDate}"
