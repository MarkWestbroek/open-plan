import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from ..enums.status import PlanStatus, Resultaat


class Ontwikkelwens(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4) voor deze functie."),
    )
    doel = models.ForeignKey(
        "plannen.Doel",
        on_delete=models.CASCADE,
        related_name="ontwikkelwensen",
        help_text=_("Het doel waaraan dit ontwikkelwens gekoppeld is."),
    )
    doel_categorieen = models.ManyToManyField(
        "plannen.DoelCategorie",
        related_name="ontwikkelwensen",
        help_text=_("Categorieën waaraan dit ontwikkelwens gekoppeld is."),
    )
    status = models.CharField(
        max_length=20,
        choices=PlanStatus.choices,
        default=PlanStatus.ACTIEF,
        help_text=_("Status van het ontwikkelwens."),
    )
    titel = models.CharField(
        max_length=255,
        help_text=_("Titel van het ontwikkelwens."),
    )
    beschrijving = models.TextField(
        blank=True,
        max_length=1000,
        help_text=_("Beschrijving van het ontwikkelwens."),
    )
    startdatum = models.DateTimeField(
        help_text=_("Startdatum van het ontwikkelwens."),
        db_index=True,
    )
    einddatum = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Einddatum van het ontwikkelwens."),
    )
    resultaat = models.CharField(
        max_length=20,
        choices=Resultaat.choices,
        blank=True,
        help_text=_("Resultaat van het ontwikkelwens."),
    )

    class Meta:
        verbose_name = "Ontwikkelwens"
        verbose_name_plural = "Ontwikkelwensen"

    def __str__(self):
        return self.titel
