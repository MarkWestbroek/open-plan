from vng_api_common.filtersets import FilterSet

from openplan.plannen.models.plan import Plan


class PlanFilter(FilterSet):
    class Meta:
        model = Plan
        fields = {
            "plantype__uuid": ["exact"],
            "overkoepelend_plan__uuid": ["exact"],
            "status": ["exact"],
            "fase": ["exact"],
            "titel": ["exact", "icontains"],
            "medewerker": ["exact"],
            "zaak": ["exact"],
            "domeinregister": ["exact"],
            "startdatum": ["exact", "gte", "lte"],
            "einddatum": ["exact", "gte", "lte"],
        }
