from django.utils.translation import gettext_lazy as _

from vng_api_common.filtersets import FilterSet

from openplan.plannen.models.ontwikkelwens import Ontwikkelwens
from openplan.utils.filters import UUIDFInFilter


class OntwikkelwensFilter(FilterSet):
    doel_uuid = UUIDFInFilter(
        field_name="doel__uuid",
        distinct=True,
        help_text=_("UUID's van gekoppelde doelen."),
    )

    doel_categorieen_uuids = UUIDFInFilter(
        field_name="doel_categorieen__uuid",
        distinct=True,
        help_text=_("UUID's van gekoppelde doelcategorieën."),
    )

    class Meta:
        model = Ontwikkelwens
        fields = {
            "status": ["exact"],
            "titel": ["exact", "icontains"],
            "startdatum": ["exact", "gte", "lte"],
            "einddatum": ["exact", "gte", "lte"],
            "resultaat": ["exact"],
        }
