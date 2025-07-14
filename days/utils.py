# day/utils.py
from django.db import transaction
from decimal import Decimal
from collections import defaultdict
from timeSections.utils import get_user_total_intervals_between_dates
from .models import ActivityScore  # Local import
from activities.models import Activity

def calculate_activity_points(total_seconds, activity):
    """
    Calculate points for an activity based on:
    - Deducting grace period (seconds_free)
    - Converting remaining time to hours
    - Multiplying by points_per_hour
    """
    if total_seconds <= activity.seconds_free:
        return Decimal('0.0')

    effective_seconds = total_seconds - activity.seconds_free
    effective_hours = Decimal(effective_seconds) / Decimal(3600)
    return effective_hours * activity.points_per_hour

def generate_day_scores(day):
    """
    Generates/updates ActivityScore records for a day.

    Returns:
        dict: {activity_id: (total_seconds, points)}
    """


    # Get time totals between day boundaries
    time_totals = get_user_total_intervals_between_dates(
        user=day.user,
        start_date=day.start_utc,
        end_date=day.end_utc
    )

    # Bulk fetch activities and existing scores
    activities = Activity.objects.in_bulk(time_totals.keys())
    existing_scores = {
        s.activity_id: s for s in
        ActivityScore.objects.filter(day=day, activity_id__in=time_totals.keys())
    }

    results = {}
    updates = []
    creates = []

    for activity_id, total_seconds in time_totals.items():
        if activity := activities.get(activity_id):
            points = calculate_activity_points(total_seconds, activity)
            results[activity_id] = (total_seconds, float(points))

            if activity_id in existing_scores:
                score = existing_scores[activity_id]
                score.points = points
                updates.append(score)
            else:
                creates.append(ActivityScore(
                    day=day,
                    activity=activity,
                    points=points
                ))

    # Atomic database operations
    with transaction.atomic():
        if creates:
            ActivityScore.objects.bulk_create(creates)
        if updates:
            ActivityScore.objects.bulk_update(updates, ['points'])

    return results