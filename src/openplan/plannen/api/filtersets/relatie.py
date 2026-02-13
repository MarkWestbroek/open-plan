from vng_api_common.filtersets import FilterSet

from openplan.plannen.models.relatie import Relatie


class RelatieFilter(FilterSet):
    class Meta:
        model = Relatie
        fields = {
            "persoon__uuid": ["exact"],
            "gerelateerde_persoon__uuid": ["exact"],
            "relatietype__uuid": ["exact"],
        }
