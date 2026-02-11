from django.utils.translation import gettext_lazy as _

from vng_api_common.filtersets import FilterSet

from openplan.plannen.models.plan import Plan
from openplan.utils.filters import UUIDFInFilter


class PlanFilter(FilterSet):
    plantype_uuid = UUIDFInFilter(
        field_name="plantype__uuid",
        distinct=True,
        help_text=_("UUID's van de gekoppelde plantypen."),
    )
    overkoepelend_plan_uuid = UUIDFInFilter(
        field_name="overkoepelend_plan__uuid",
        distinct=True,
        help_text=_("UUID van het overkoepelend plan."),
    )

    class Meta:
        model = Plan
        fields = {
            "status": ["exact"],
            "fase": ["exact"],
            "titel": ["exact", "icontains"],
            "medewerker": ["exact"],
            "zaak": ["exact"],
            "domeinregister": ["exact"],
            "startdatum": ["exact", "gte", "lte"],
            "einddatum": ["exact", "gte", "lte"],
        }
