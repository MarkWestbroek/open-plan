import uuid

from django.db import models

from vng_api_common.fields import BSNField

from openplan.utils.fields import URIField


class Persoon(models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )
    persoonsprofiel = URIField(
        blank=True,
        help_text="URI naar het persoonsprofiel "
        "(alleen voor primaire personen verplicht).",
    )
    klant = URIField(
        blank=True,
        help_text="URI naar de Klant "
        "(verplicht voor primaire personen, optioneel voor secundaire).",
    )
    bsn = BSNField(
        blank=True,
        help_text="BSN voor BRP-koppeling "
        "(verplicht voor primaire personen, optioneel voor secundaire).",
    )

    class Meta:
        verbose_name = "Persoon"
        verbose_name_plural = "Personen"

    def __str__(self):
        return f"Persoon {self.uuid}"
