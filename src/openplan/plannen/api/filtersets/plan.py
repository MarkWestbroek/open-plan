from django.utils.translation import gettext_lazy as _

from openplan.plannen.models.plan import Plan
from openplan.utils.filters import (
    FilterSet,
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
