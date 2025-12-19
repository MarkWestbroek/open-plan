import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from openplan.utils.fields import URIField


class Plan(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4) voor deze functie."),
    )
    plantype = models.ForeignKey(
        "plannen.Plantype",
        on_delete=models.PROTECT,
        help_text=_("Type van het plan."),
    )
    zaak = URIField(
        help_text=_("URI naar de bijbehorende zaak in het zaaksysteem."),
        blank=True,
    )
    domeinregister = URIField(
        help_text=_("URI naar het domeinregister voor dit plan."),
        blank=True,
    )
    # TODO:
    # Multiple uri's???
    medewerker = URIField(
        help_text=_("URI naar de medewerker in het HR-systeem."),
        blank=True,
    )

    class Meta:
        verbose_name = _("Plan")
        verbose_name_plural = _("Plannen")

    def __str__(self):
        return str(self.plantype)
