import uuid

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class StableModel(models.Model):
    """Basis voor alle entiteiten met een stabiele identiteit."""

    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4)."),
    )

    class Meta:
        abstract = True

    @property
    def current_state(self):
        """Huidige state van dit object."""
        qs = getattr(self, "states", None)
        if qs:
            now = timezone.now()
            return (
                qs.filter(startdatum__lte=now)
                .filter(Q(einddatum__gt=now) | Q(einddatum__isnull=True))
                .first()
            )
        return None


class StateModel(models.Model):
    """Abstract base class voor alle state-modellen."""

    startdatum = models.DateTimeField()
    einddatum = models.DateTimeField(null=True, blank=True)

    recorded_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        abstract = True
        ordering = ["startdatum"]
