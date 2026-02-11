from django.utils.translation import gettext_lazy as _

from vng_api_common.filtersets import FilterSet

from openplan.plannen.models.doel import Doel
from openplan.utils.filters import UUIDFInFilter


class DoelFilter(FilterSet):
    doeltype_uuid = UUIDFInFilter(
        field_name="doeltype__uuid",
        distinct=True,
        help_text=_("UUID's van de gekoppelde doeltypen."),
    )
    persoon_uuid = UUIDFInFilter(
        field_name="persoon__uuid",
        distinct=True,
        help_text=_("UUID's van de gekoppelde personen."),
    )
    plannen_uuids = UUIDFInFilter(
        field_name="plannen__uuid",
        distinct=True,
        help_text=_("UUID's van de gekoppelde plannen."),
    )
    hoofd_doel_uuid = UUIDFInFilter(
        field_name="hoofd_doel__uuid",
        distinct=True,
        help_text=_("UUID's van de bovenliggende doelen."),
    )

    class Meta:
        model = Doel
        fields = {
            "status": ["exact", "in"],
            "titel": ["exact", "icontains"],
            "startdatum": ["exact", "gte", "lte"],
            "einddatum": ["exact", "gte", "lte"],
            "resultaat": ["exact"],
        }
