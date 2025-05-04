from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator  # Added import
import uuid

User = get_user_model()

class Activity(models.Model):
    # Define validator at class level
    hex_color_validator = RegexValidator(
        regex=r'^#[0-9a-fA-F]{6}$',
        message="Enter a valid hex color code (e.g., #32a852)."
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    color = models.CharField(
        max_length=7,
        default='#000000',
        validators=[hex_color_validator],
    )

    name = models.CharField(
        max_length=100,
    )

    icon = models.CharField(
        max_length=50,
        blank=True,
        default=''
    )

    points_per_hour = models.FloatField(
        default=0.0
    )

    seconds_free = models.PositiveIntegerField(
        default=0
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='activities'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Activity"  # Added singular name
        verbose_name_plural = "Activities"
        ordering = ['-created_at']
        constraints = [
        models.UniqueConstraint(
            fields=['user', 'name'],
            name='unique_activity_name_per_user',
            condition=models.Q(name__iexact=models.F('name'))  # Case-insensitive DB-level
        )
    ]

    def clean(self):
        """Case-insensitive name validation"""
        if Activity.objects.filter(
            user=self.user,
            name__iexact=self.name
        ).exclude(id=self.id).exists():  # Changed pk to id
            raise ValidationError('An activity with this name already exists (case insensitive).')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.user.username})"