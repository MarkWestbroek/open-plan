import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from openplan.plannen.enums.status import PlanStatus, Resultaat
from openplan.utils.fields import URNField


class Instrument(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4) voor deze functie."),
    )
    doelen = models.ManyToManyField(
        "plannen.Doel",
        blank=True,
        related_name="instrumenten",
        help_text=_("Doelen waaraan dit instrument gekoppeld is."),
    )
    ontwikkelwensen = models.ManyToManyField(
        "plannen.Ontwikkelwens",
        blank=True,
        related_name="instrumenten",
        help_text=_("Ontwikkelwensen waaraan dit instrument gekoppeld is."),
    )
    status = models.CharField(
        max_length=20,
        choices=PlanStatus.choices,
        default=PlanStatus.ACTIEF,
        help_text=_("Status van het instrument."),
    )
    instrumenttype = models.ForeignKey(
        "plannen.Instrumenttype",
        on_delete=models.PROTECT,
        help_text=_("Het type instrument dat hier wordt toegepast."),
    )
    instrument_categorieen = models.ManyToManyField(
        "plannen.InstrumentCategorie",
        related_name="instrumenten",
        help_text=_("Categorieen van het instrument."),
    )
    titel = models.CharField(
        max_length=255,
        help_text=_("Titel van het instrument."),
    )
    startdatum = models.DateTimeField(
        help_text=_("Startdatum van het instrument."),
        db_index=True,
    )
    einddatum = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Einddatum van het instrument."),
    )
    resultaat = models.CharField(
        max_length=20,
        choices=Resultaat.choices,
        blank=True,
        help_text=_("Resultaat van het instrument."),
    )

    product = URNField(
        help_text=_("URN naar de bijbehorende product in het productsysteem."),
        blank=True,
    )
    zaak = URNField(
        help_text=_("URN naar het bijbehorende zaak in het zaaksysteem."),
        blank=True,
    )

    class Meta:
        verbose_name = _("Instrument")
        verbose_name_plural = _("Instrumenten")

    def __str__(self):
        return str(self.uuid)
