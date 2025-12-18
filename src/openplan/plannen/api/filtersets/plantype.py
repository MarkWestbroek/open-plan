from openplan.plannen.models.plantype import PlanType
from openplan.utils.filters import (
    FilterSet,
)


class PlanTypeFilter(FilterSet):
    class Meta:
        model = PlanType
        fields = {
            "type": ["exact"],
        }
