from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_hoofd_doel_not_self(doel):
    if doel.hoofd_doel and doel.hoofd_doel == doel:
        raise ValidationError(
            {"hoofd_doel": _("Een doel kan niet naar zichzelf verwijzen.")}
        )

    parent = doel.hoofd_doel
    while parent:
        if parent == doel:
            raise ValidationError(
                {
                    "hoofd_doel": _(
                        "Een hoofd doel kan geen kind als bovenliggende doel hebben."
                    )
                }
            )
        parent = parent.hoofd_doel


def validate_primary_persoon(persoon):
    errors = []
    if not persoon.persoonsprofiel_url:
        errors.append(_("Primair persoon moet een persoonsprofiel URL hebben."))
    if not persoon.open_klant_url:
        errors.append(_("Primair persoon moet een Open Klant koppeling hebben."))
    if not persoon.bsn:
        errors.append(_("Primair persoon moet een BRP-koppeling (BSN) hebben."))

    if errors:
        raise ValidationError({"persoon": errors})


def validate_relatie_uniqueness(relatie):
    if relatie.persoon == relatie.gerelateerde_persoon:
        raise ValidationError(_("Een persoon kan geen relatie met zichzelf hebben."))

    if relatie.__class__.objects.filter(
        persoon=relatie.gerelateerde_persoon,
        gerelateerde_persoon=relatie.persoon,
        relatietype=relatie.relatietype,
    ).exists():
        raise ValidationError(_("Deze relatie bestaat al in omgekeerde richting."))
