from django.utils.translation import gettext_lazy as _

from vng_api_common.filtersets import FilterSet

from openplan.plannen.models.instrument import Instrument
from openplan.utils.filters import UUIDFInFilter


class InstrumentFilter(FilterSet):
    doelen__uuid__in = UUIDFInFilter(
        field_name="doelen__uuid",
        distinct=True,
        help_text=_("UUID's van gekoppelde doelen."),
    )

    ontwikkelwensen__uuid__in = UUIDFInFilter(
        field_name="ontwikkelwensen__uuid",
        distinct=True,
        help_text=_("UUID's van gekoppelde ontwikkelwensen."),
    )

    instrument_categorieen__uuid__in = UUIDFInFilter(
        field_name="instrument_categorieen__uuid",
        distinct=True,
        help_text=_("UUID's van gekoppelde instrumentcategorieën."),
    )

    class Meta:
        model = Instrument
        fields = {
            "doelen__uuid": ["exact"],
            "ontwikkelwensen__uuid": ["exact"],
            "instrument_categorieen__uuid": ["exact"],
            "instrumenttype__uuid": ["exact"],
            "status": ["exact"],
            "titel": ["exact", "icontains"],
            "resultaat": ["exact"],
            "product": ["exact"],
            "zaak": ["exact"],
            "startdatum": ["exact", "gte", "lte"],
            "einddatum": ["exact", "gte", "lte"],
        }
