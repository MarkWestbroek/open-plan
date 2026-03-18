from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from openplan.utils.fields import URNField
from openplan.utils.state import TemporalManager

from ..enums.status import PlanStatus
from .state import StableModel, StateModel


class Plan(StableModel):
    overkoepelend_plan = models.ForeignKey(
        "plannen.Overkoepelendplan",
        on_delete=models.PROTECT,
        related_name="plannen",
        help_text=_("Het overkoepelend plan waar dit plan deel van uitmaakt."),
    )
    plantype = models.ForeignKey(
        "plannen.Plantype",
        on_delete=models.PROTECT,
        help_text=_("Type van het plan."),
    )
    zaak = URNField(
        help_text=_("URN naar de bijbehorende zaak in het zaaksysteem."),
        blank=True,
    )
    domeinregister = URNField(
        help_text=_("URN naar het domeinregister voor dit plan."),
        blank=True,
    )
    # TODO:
    # Multiple uri's???
    medewerker = URNField(
        help_text=_("URN naar de medewerker in het HR-systeem."),
        blank=True,
    )
    startdatum = models.DateTimeField(
        default=timezone.now,
        help_text=_("Startdatum van het plan."),
        db_index=True,
    )

    class Meta:
        verbose_name = _("Plan")
        verbose_name_plural = _("Plannen")
        ordering = ("-startdatum",)

    def __str__(self):
        return str(self.plantype)


class PlanState(StateModel):
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name="states",
    )

    titel = models.CharField(max_length=255)
    notitie = models.TextField(blank=True, max_length=1000)
    status = models.CharField(max_length=20, choices=PlanStatus.choices)
    fase = models.CharField(max_length=20, choices=PlanStatus.choices)
    reden_einde = models.TextField(blank=True, max_length=1000)

    objects = TemporalManager()

    @staticmethod
    def stable_field_name():
        return "plan"

    class Meta:
        verbose_name = _("Plan State")
        verbose_name_plural = _("Plan States")
        ordering = ["startdatum"]
        indexes = [
            models.Index(fields=["plan", "startdatum"]),
            models.Index(fields=["einddatum"]),
        ]
