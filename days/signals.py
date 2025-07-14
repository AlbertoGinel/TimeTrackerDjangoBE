# days/signals.py
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Day

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_days(sender, instance, created, **kwargs):
    if created:
        Day.ensure_year_ahead(instance)


@receiver(post_save, sender=Day)
def handle_day_closure(sender, instance, **kwargs):
    if instance.end_utc <= timezone.now():
        ActivityScoreCalculator.finalize_day_scores(instance)

        """