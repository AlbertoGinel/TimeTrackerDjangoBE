@shared_task
def update_live_scores():
    open_days = Day.objects.filter(end_utc__gt=timezone.now())
    for day in open_days:
        for activity in day.user.activities.all():
            score = ActivityScoreCalculator.calculate_dynamic_score(day, activity)
            cache.set(f"live_score:{day.id}:{activity.id}", score)  # Temporary storage