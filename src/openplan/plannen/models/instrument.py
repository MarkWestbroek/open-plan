import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Instrument(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4) voor deze functie."),
    )
    doel = models.ForeignKey(
        "plannen.Doel",
        on_delete=models.CASCADE,
        related_name="instrumenten",
        help_text=_("Het doel waaraan dit instrument gekoppeld is."),
    )
    instrumenttype = models.ForeignKey(
        "plannen.Instrumenttype",
        on_delete=models.PROTECT,
        help_text=_("Het type instrument dat hier wordt toegepast."),
    )
    # TODO:
    # Link to Open Product - Open Zaak?

    class Meta:
        verbose_name = _("Instrument")
        verbose_name_plural = _("Instrumenten")

    def __str__(self):
        return str(self.uuid)
