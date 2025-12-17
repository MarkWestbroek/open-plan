import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import validate_relatie_uniqueness


class Relatie(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4) voor deze functie."),
    )
    persoon = models.ForeignKey(
        "plannen.Persoon",
        on_delete=models.CASCADE,
        related_name="relaties_vanuit",
        help_text=_("De primaire persoon van wie de relatie is."),
    )

    gerelateerde_persoon = models.ForeignKey(
        "plannen.Persoon",
        on_delete=models.CASCADE,
        related_name="relaties_naar",
        help_text=_("De persoon naar wie de relatie gericht is."),
    )

    relatietype = models.ForeignKey(
        "plannen.Relatietype",
        on_delete=models.PROTECT,
        help_text=_("Het type relatie tussen de betrokken personen."),
    )

    class Meta:
        verbose_name = _("Relatie")
        verbose_name_plural = _("Relaties")

        constraints = [
            models.UniqueConstraint(
                fields=["persoon", "gerelateerde_persoon", "relatietype"],
                name="unieke_relaties_tussen_personen",
            )
        ]

    def __str__(self):
        return f"{self.persoon} - {self.relatietype} - {self.gerelateerde_persoon}"

    def clean(self):
        validate_relatie_uniqueness(self)
