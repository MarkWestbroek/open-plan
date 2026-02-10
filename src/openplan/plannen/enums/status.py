from django.db import models
from django.utils.translation import gettext_lazy as _


class PlanStatus(models.TextChoices):
    ACTIEF = "actief", _("Actief")
    AFGEROND = "afgerond", _("Afgerond")
    GEANNULEERD = "geannuleerd", _("Geannuleerd")


class Resultaat(models.TextChoices):
    BEHAALD = "behaald", _("Behaald")
    GEFAALD = "gefaald", _("Gefaald")
