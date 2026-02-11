import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class DoelCategorie(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4)."),
    )
    naam = models.CharField(
        max_length=200,
        unique=True,
        help_text=_("Naam van de doelcategorie."),
    )

    class Meta:
        verbose_name = _("Doelcategorie")
        verbose_name_plural = _("Doelcategorieen")

    def __str__(self):
        return self.naam
