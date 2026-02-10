import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from openplan.plannen.enums.status import PlanStatus
from openplan.utils.fields import URNField


class OverkoepelendPlan(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
    )
    titel = models.CharField(
        max_length=255,
        help_text=_("Titel van het overkoepelende plan."),
    )
    status = models.CharField(
        max_length=20,
        choices=PlanStatus.choices,
        default=PlanStatus.ACTIEF,
        help_text=_("Status van het overkoepelende plan."),
    )
    medewerker = URNField(
        help_text=_("URN naar de medewerker in het HR-systeem."),
        blank=True,
    )

    class Meta:
        verbose_name = _("Overkoepelend plan")
        verbose_name_plural = _("Overkoepelende plannen")

    def __str__(self):
        return self.titel
