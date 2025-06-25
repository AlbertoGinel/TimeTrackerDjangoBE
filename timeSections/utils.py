# Utility to generate intervals from stamps
# timeSections/utils.py
from .models import Stamp, Interval

def get_user_intervals(user):
    """Converts a user's stamps into intervals (no DB queries for Interval)."""
    stamps = Stamp.objects.filter(user=user).order_by('timestamp')
    intervals = []
    open_interval = None

    for stamp in stamps:
        if stamp.type == Stamp.StampType.START:
            if open_interval:
                # Close previous interval (interrupted by new START)
                intervals.append(Interval(
                    open_interval.opening_stamp,
                    closing_stamp=stamp  # Closed by START (switch)
                ))
            open_interval = Interval(opening_stamp=stamp)  # New interval
        else:  # STOP stamp
            if open_interval:
                intervals.append(Interval(
                    open_interval.opening_stamp,
                    closing_stamp=stamp
                ))
                open_interval = None
            # Else: Orphaned STOP (handle as needed)

    # Add the last open interval (if any)
    if open_interval:
        intervals.append(open_interval)

    return intervals