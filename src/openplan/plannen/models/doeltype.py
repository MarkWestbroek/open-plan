import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from ..enums.doel import DoelTypeEnum


class DoelType(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4) voor deze functie."),
    )
    type = models.CharField(
        max_length=50,
        choices=DoelTypeEnum.choices,
        unique=True,
        help_text=_("De unieke naam van dit doeltype."),
    )

    class Meta:
        verbose_name = "Doeltype"
        verbose_name_plural = "Doeltypen"

    def __str__(self):
        return self.type
