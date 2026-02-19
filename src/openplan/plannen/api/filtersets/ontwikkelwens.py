from django.utils.translation import gettext_lazy as _

from vng_api_common.filtersets import FilterSet

from openplan.plannen.models.ontwikkelwens import Ontwikkelwens
from openplan.utils.filters import UUIDFInFilter


class OntwikkelwensFilter(FilterSet):
    doel_categorieen__uuid__in = UUIDFInFilter(
        field_name="doel_categorieen__uuid",
        distinct=True,
        help_text=_("UUID's van gekoppelde doelcategorieën."),
    )

    class Meta:
        model = Ontwikkelwens
        fields = {
            "doel__uuid": ["exact"],
            "doel_categorieen__uuid": ["exact"],
            "status": ["exact"],
            "titel": ["exact", "icontains"],
            "startdatum": ["exact", "gte", "lte"],
            "einddatum": ["exact", "gte", "lte"],
            "resultaat": ["exact"],
        }
