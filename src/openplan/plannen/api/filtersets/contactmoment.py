from django.utils.translation import gettext_lazy as _

from vng_api_common.filtersets import FilterSet

from openplan.plannen.models.contactmoment import Contactmoment
from openplan.utils.filters import UUIDFInFilter


class ContactmomentFilter(FilterSet):
    plan_uuid = UUIDFInFilter(
        field_name="plan__uuid",
        distinct=True,
        help_text=_("UUID van het gekoppelde plan."),
    )

    class Meta:
        model = Contactmoment
        fields = {
            "status": ["exact"],
            "datum": ["exact", "gte", "lte"],
            "persoonsprofiel": ["exact", "icontains"],
        }
