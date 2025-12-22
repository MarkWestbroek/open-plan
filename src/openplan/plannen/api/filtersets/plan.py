from django.utils.translation import gettext_lazy as _

from vng_api_common.filtersets import FilterSet

from openplan.plannen.models.plan import Plan
from openplan.utils.filters import (
    UUIDFInFilter,
)


class PlanFilter(FilterSet):
    plantype_uuid = UUIDFInFilter(
        field_name="plantype__uuid",
        lookup_expr="in",
        distinct=True,
        help_text=_("UUID's van de gekoppelde plantypen."),
    )

    class Meta:
        model = Plan
        fields = {}
