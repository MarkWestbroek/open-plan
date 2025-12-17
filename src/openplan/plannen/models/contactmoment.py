import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Contactmoment(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4) voor deze functie."),
    )
    plan = models.ForeignKey(
        "plannen.Plan",
        on_delete=models.CASCADE,
        related_name="contactmomenten",
        help_text=_("Het plan waarbij dit contactmoment hoort."),
    )

    # TODO:
    # Link to domeinen

    class Meta:
        verbose_name = _("Contactmoment")
        verbose_name_plural = _("Contactmomenten")

    def __str__(self):
        return str(self.uuid)
