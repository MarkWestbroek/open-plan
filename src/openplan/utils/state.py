from django.db import models
from django.db.models import Q
from django.utils import timezone


class TemporalQuerySet(models.QuerySet):
    def current(self):
        now = timezone.now()
        return self.filter(startdatum__lte=now).filter(
            Q(einddatum__gt=now) | Q(einddatum__isnull=True)
        )

    def at(self, dt):
        return self.filter(startdatum__lte=dt).filter(
            Q(einddatum__gt=dt) | Q(einddatum__isnull=True)
        )

    def history(self):
        return self.order_by("startdatum")


class TemporalManager(models.Manager):
    def get_queryset(self):
        return TemporalQuerySet(self.model, using=self._db)

    def current(self):
        return self.get_queryset().current()

    def at(self, dt):
        return self.get_queryset().at(dt)

    def history(self):
        return self.get_queryset().history()


def create_state(
    stable_obj,
    state_model,
    user,
    startdatum=None,
    **fields,
):
    if startdatum is None:
        startdatum = timezone.now()

    # Sluit huidige state
    current = state_model.objects.filter(
        **{state_model.stable_field_name(): stable_obj}, einddatum__isnull=True
    ).first()

    if current:
        current.einddatum = startdatum
        current.save()

    # Maak nieuwe state
    return state_model.objects.create(
        **{state_model.stable_field_name(): stable_obj},
        startdatum=startdatum,
        changed_by=user,
        **fields,
    )
