import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class RelatieType(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4) voor deze functie."),
    )
    naam = models.CharField(
        max_length=100,
        unique=True,
        help_text=_("Naam van het relatietype"),
    )

    class Meta:
        verbose_name = _("Relatietype")
        verbose_name_plural = _("Relatietypen")

    def __str__(self):
        return self.naam
