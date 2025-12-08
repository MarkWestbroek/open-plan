import uuid

from django.db import models


class Persoon(models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )
    # TODO:
    # Fix this later
    persoonsprofiel_url = models.URLField(
        blank=True,
        help_text="URL naar het persoonsprofiel "
        "(alleen voor primaire personen verplicht).",
    )
    open_klant_url = models.URLField(
        blank=True,
        help_text="URL naar Open Klant "
        "(verplicht voor primaire personen, optioneel voor secundaire).",
    )
    bsn = models.CharField(
        max_length=9,
        blank=True,
        help_text="BSN voor BRP-koppeling "
        "(verplicht voor primaire personen, optioneel voor secundaire).",
    )

    class Meta:
        verbose_name = "Persoon"
        verbose_name_plural = "Personen"

    def __str__(self):
        return f"Persoon {self.uuid}"
