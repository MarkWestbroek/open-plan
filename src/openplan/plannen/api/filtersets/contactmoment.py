from vng_api_common.filtersets import FilterSet

from openplan.plannen.models.contactmoment import Contactmoment


class ContactmomentFilter(FilterSet):
    class Meta:
        model = Contactmoment
        fields = {
            "plan__uuid": ["exact"],
            "status": ["exact"],
            "datum": ["exact", "gte", "lte"],
            "persoonsprofiel": ["exact", "icontains"],
        }
