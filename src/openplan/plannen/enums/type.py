from django.db import models
from django.utils.translation import gettext_lazy as _


class PlanTypeEnum(models.TextChoices):
    INBURGERING = (
        "PIP",
        _("Persoonlijk plan inburgering en perticipatie"),
    )
    WERK = (
        "Werk",
        _("Werk"),
    )
    INKOMEN = (
        "Inkomen",
        _("Inkomen"),
    )


class InstrumentTypeEnum(models.TextChoices):
    # voorbeelden
    TRAINING = (
        "Training",
        _("Training"),
    )
    COACHING = (
        "Coaching",
        _("Coaching"),
    )
    FINANCIËLE_STEUNING = (
        "Financiële ondersteuning",
        _("Financiële ondersteuning"),
    )
