from django.utils.translation import gettext_lazy as _

from vng_api_common.filtersets import FilterSet

from openplan.plannen.models.relatie import Relatie
from openplan.utils.filters import UUIDFInFilter


class RelatieFilter(FilterSet):
    persoon_uuid = UUIDFInFilter(
        field_name="persoon__uuid",
        distinct=True,
        help_text=_("UUID van de primaire persoon."),
    )
    gerelateerde_persoon_uuid = UUIDFInFilter(
        field_name="gerelateerde_persoon__uuid",
        distinct=True,
        help_text=_("UUID van de gerelateerde persoon."),
    )
    relatietype_uuid = UUIDFInFilter(
        field_name="relatietype__uuid",
        help_text=_("UUID van het relatietype."),
    )

    class Meta:
        model = Relatie
        fields = {}
