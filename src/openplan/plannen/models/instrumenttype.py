import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from ..enums.type import InstrumentTypeEnum


class InstrumentType(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4) voor deze functie."),
    )
    instrument_type = models.CharField(
        choices=InstrumentTypeEnum.choices,
        max_length=50,
        help_text=_("Het type instrument."),
    )
    categorieen = models.ManyToManyField(
        "plannen.InstrumentCategorie",
        related_name="instrumenttypes",
        help_text=_("Categorieën waaraan dit instrumenttype gekoppeld is."),
    )

    class Meta:
        verbose_name = _("Instrumenttype")
        verbose_name_plural = _("Instrumenttypen")

    def __str__(self):
        return self.instrument_type
