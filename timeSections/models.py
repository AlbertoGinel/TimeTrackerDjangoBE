from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()

class Stamp(models.Model):
    class StampType(models.TextChoices):
        START = 'start', 'Start'
        STOP = 'stop', 'Stop'

    type = models.CharField(
        max_length=5,
        choices=StampType.choices,
        default=StampType.START
    )
    timestamp = models.DateTimeField(default=timezone.now)
    activity = models.ForeignKey(
        'activities.Activity',
        on_delete=models.CASCADE,
        related_name='stamps'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='stamps'
    )

    class Meta:
        ordering = ['-timestamp']  # Newest stamps first
        indexes = [
            models.Index(fields=['user', 'activity']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.type} at {self.timestamp}"

    def clean(self):
        if self.user != self.activity.user:
            raise ValidationError("Stamp user must match activity user.")
