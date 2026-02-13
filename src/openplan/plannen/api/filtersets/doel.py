from django.utils.translation import gettext_lazy as _

from vng_api_common.filtersets import FilterSet

from openplan.plannen.models.doel import Doel
from openplan.utils.filters import UUIDFInFilter


class DoelFilter(FilterSet):
    plannen__uuid__in = UUIDFInFilter(
        field_name="plannen__uuid",
        distinct=True,
        help_text=_("UUID's van de gekoppelde plannen."),
    )

    class Meta:
        model = Doel
        fields = {
            "plannen__uuid": ["exact"],
            "doeltype__uuid": ["exact"],
            "persoon__uuid": ["exact"],
            "hoofd_doel__uuid": ["exact"],
            "status": ["exact", "in"],
            "titel": ["exact", "icontains"],
            "startdatum": ["exact", "gte", "lte"],
            "einddatum": ["exact", "gte", "lte"],
            "resultaat": ["exact"],
        }
