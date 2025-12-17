from django.db import models
from django.utils.translation import gettext_lazy as _


class DoelTypeEnum(models.TextChoices):
    HOOFDDOEL = "hoofddoel", _("Hoofddoel")
    SUBDOEL = "subdoel", _("Subdoel")
    ONTWIKKELWENS = "ontwikkelwens", _("Ontwikkelwens")


class HoofddoelEnum(models.TextChoices):
    BETAALDWERKEN = "betaald_werken", _("Betaald werken")
    ONDERNEMEN = "ondernemen", _("Ondernemen")
    OPLEIDINGMETSTUDIEFINANCIERING = (
        "opleiding_met_studiefinanciering",
        _("Opleiding met studiefinanciering"),
    )

    BETAALDWERKENNAARVERMOGEN = (
        "betaald_werken_naar_vermogen",
        _("Betaald werken naar vermogen"),
    )
    WERKFITWORDEN = ("werkfit_worden", _("Werkfit worden"))
    MAATSCHAPPELIJKFITWORDEN = (
        "maatschappelijk_fit_worden",
        _("Maatschappelijk fit worden"),
    )
