import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class InstrumentCategorie(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4) voor deze categorie."),
    )
    naam = models.CharField(
        max_length=200,
        unique=True,
        help_text=_("Naam van de instrumentcategorie."),
    )

    class Meta:
        verbose_name = _("Instrumentcategorie")
        verbose_name_plural = _("Instrumentcategorieen")

    def __str__(self):
        return self.naam
