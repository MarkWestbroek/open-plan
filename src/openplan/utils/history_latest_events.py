from django.db.models import QuerySet


def latest_events_at(qs: QuerySet, at):
    """
    Returns the latest event per object before timestamp `at`
    """
    return (
        qs.filter(pgh_created_at__lte=at)
        .order_by("pgh_obj_id", "-pgh_created_at")
        .distinct("pgh_obj_id")
    )
