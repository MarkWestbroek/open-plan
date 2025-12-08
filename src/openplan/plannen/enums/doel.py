from django.db import models
from django.utils.translation import gettext_lazy as _


class DoelTypeEnum(models.TextChoices):
    HOOFDDOEL = "Hoofddoel", _("Hoofddoel")
    SUBDOEL = "Subdoel", _("Subdoel")
    ONTWIKKELWENS = "Ontwikkelwens", _("Ontwikkelwens")


class HoofddoelEnum(models.TextChoices):
    BETAALDWERKEN = "Betaald werken", _("Betaald werken")
    ONDERNEMEN = "Ondernemen", _("Ondernemen")
    OPLEIDINGMETSTUDIEFINANCIERING = (
        "Opleiding met studiefinanciering",
        _("Opleiding met studiefinanciering"),
    )

    BETAALDWERKENNAARVERMOGEN = (
        "Betaald werken naar vermogen",
        _("Betaald werken naar vermogen"),
    )
    WERKFITWORDEN = ("Werkfit worden", _("Werkfit worden"))
    MAATSCHAPPELIJKFITWORDEN = (
        "Maatschappelijk fit worden",
        _("Maatschappelijk fit worden"),
    )
