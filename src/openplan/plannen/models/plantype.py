import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from ..enums.type import PlanTypeEnum


class PlanType(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4) voor deze functie."),
    )
    type = models.CharField(
        choices=PlanTypeEnum.choices,
        max_length=50,
        unique=True,
        help_text=_("Het type plan."),
    )

    class Meta:
        verbose_name = _("Plantype")
        verbose_name_plural = _("Plantypen")

    def __str__(self):
        return str(self.type)
