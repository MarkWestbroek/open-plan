from django.utils.translation import gettext_lazy as _

from vng_api_common.filtersets import FilterSet

from openplan.plannen.models.instrument import Instrument
from openplan.utils.filters import UUIDFInFilter


class InstrumentFilter(FilterSet):
    doelen_uuids = UUIDFInFilter(
        field_name="doelen__uuid",
        distinct=True,
        help_text=_("UUID's van gekoppelde doelen."),
    )

    ontwikkelwensen_uuids = UUIDFInFilter(
        field_name="ontwikkelwensen__uuid",
        distinct=True,
        help_text=_("UUID's van gekoppelde ontwikkelwensen."),
    )

    instrumenttype_uuid = UUIDFInFilter(
        field_name="instrumenttype__uuid",
        help_text=_("UUID van het instrumenttype."),
    )

    instrument_categorieen_uuids = UUIDFInFilter(
        field_name="instrument_categorieen__uuid",
        distinct=True,
        help_text=_("UUID's van gekoppelde instrumentcategorieën."),
    )

    class Meta:
        model = Instrument
        fields = {
            "status": ["exact"],
            "titel": ["exact", "icontains"],
            "resultaat": ["exact"],
            "product": ["exact"],
            "zaak": ["exact"],
            "startdatum": ["exact", "gte", "lte"],
            "einddatum": ["exact", "gte", "lte"],
        }
