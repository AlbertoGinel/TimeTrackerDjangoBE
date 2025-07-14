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



def get_user_intervals_between_dates(user, start_date, end_date=None):
    """
    Efficiently gets intervals between two dates by querying only relevant stamps.
    """
    if end_date is None:
        end_date = timezone.now()

    # Get stamps in the date range plus potentially overlapping ones
    stamps = Stamp.objects.filter(
        user=user,
        timestamp__gte=start_date - timedelta(days=1),  # Include stamps slightly before
        timestamp__lte=end_date + timedelta(days=1)     # Include stamps slightly after
    ).order_by('timestamp')

    intervals = []
    open_interval = None
    prev_stamp = None

    for stamp in stamps:
        # Skip stamps that are completely outside our range (the buffer catches overlaps)
        if stamp.timestamp < start_date:
            prev_stamp = stamp
            continue
        if stamp.timestamp > end_date:
            break

        if stamp.type == Stamp.StampType.START:
            if open_interval:
                # Close previous interval at either: the new START or our end_date
                close_time = min(stamp.timestamp, end_date)
                if open_interval.fromDate < close_time:
                    intervals.append(Interval(
                        open_interval.opening_stamp,
                        closing_stamp=Stamp(  # Create a fake stamp for the boundary
                            type=Stamp.StampType.STOP,
                            timestamp=close_time,
                            user=user,
                            activity=open_interval.activity
                        ) if stamp.timestamp > end_date else stamp
                    ))
            
            # Start new interval at either: the stamp time or our start_date
            start_time = max(stamp.timestamp, start_date)
            if start_time < end_date:
                fake_start = Stamp(
                    type=Stamp.StampType.START,
                    timestamp=start_time,
                    user=user,
                    activity=stamp.activity
                ) if stamp.timestamp < start_date else stamp
                open_interval = Interval(opening_stamp=fake_start)
        
        else:  # STOP stamp
            if open_interval:
                # Close at either: the STOP time or our end_date
                close_time = min(stamp.timestamp, end_date)
                if open_interval.fromDate < close_time:
                    intervals.append(Interval(
                        open_interval.opening_stamp,
                        closing_stamp=Stamp(
                            type=Stamp.StampType.STOP,
                            timestamp=close_time,
                            user=user,
                            activity=open_interval.activity
                        ) if stamp.timestamp > end_date else stamp
                    ))
                open_interval = None
            # Else: Orphaned STOP (could handle if needed)

    # Handle the last open interval if it extends into our range
    if open_interval and open_interval.fromDate < end_date:
        intervals.append(Interval(
            open_interval.opening_stamp,
            closing_stamp=Stamp(
                type=Stamp.StampType.STOP,
                timestamp=end_date,
                user=user,
                activity=open_interval.activity
            )
        ))

    return intervals


from collections import defaultdict

def get_user_total_intervals_between_dates(user, start_date, end_date=None):
    """
    Returns activity totals between dates in format:
    {
        activity_id: total_seconds,
        ...
    }
    """
    intervals = get_user_intervals_between_dates(user, start_date, end_date)
    activity_totals = defaultdict(float)  # Using float to accumulate seconds
    
    for interval in intervals:
        if interval.activity:  # Only count intervals with activities
            duration = interval.duration.total_seconds()
            activity_totals[interval.activity.id] += duration
    
    return dict(activity_totals)

