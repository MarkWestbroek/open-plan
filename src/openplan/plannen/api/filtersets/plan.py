from openplan.plannen.models.plan import Plan
from openplan.utils.filters import (
    FilterSet,
)


class PlanFilter(FilterSet):
    class Meta:
        model = Plan
        fields = {
            "plantype": ["exact"],
        }
