import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from openplan.utils.fields import URNField

from ..enums.status import PlanStatus


class Plan(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4)."),
    )
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
    status = models.CharField(
        max_length=20,
        choices=PlanStatus.choices,
        default=PlanStatus.ACTIEF,
        help_text=_("Status van het plan."),
    )
    fase = models.CharField(
        max_length=20,
        choices=PlanStatus.choices,
        default=PlanStatus.ACTIEF,
        help_text=_("Fase van het plan."),
    )
    titel = models.CharField(
        max_length=255,
        help_text=_("Titel van het plan."),
    )
    notitie = models.TextField(
        blank=True,
        max_length=1000,
        help_text=_("Notitie bij het plan."),
    )
    startdatum = models.DateTimeField(
        help_text=_("Startdatum van het plan."),
        db_index=True,
    )
    einddatum = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Einddatum van het plan."),
    )
    reden_einde = models.TextField(
        blank=True,
        max_length=1000,
        help_text=_("Reden waarom het plan is beëindigd."),
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

    class Meta:
        verbose_name = _("Plan")
        verbose_name_plural = _("Plannen")
        ordering = ("-startdatum",)

    def __str__(self):
        return str(self.plantype)
