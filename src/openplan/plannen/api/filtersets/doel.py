from django.utils.translation import gettext_lazy as _

from vng_api_common.filtersets import FilterSet

from openplan.plannen.models.doel import Doel
from openplan.utils.filters import (
    UUIDFInFilter,
)


class DoelFilter(FilterSet):
    doeltype_uuid = UUIDFInFilter(
        field_name="doeltype__uuid",
        lookup_expr="in",
        distinct=True,
        help_text=_("UUID's van de gekoppelde doeltypen."),
    )

    class Meta:
        model = Doel
        fields = {}
