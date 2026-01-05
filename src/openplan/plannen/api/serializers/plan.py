from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openplan.plannen.models.plan import Plan
from openplan.plannen.models.plantype import PlanType
from openplan.utils.fields import UUIDRelatedField
from openplan.utils.serializers import URNModelSerializer

from .plantype import PlanTypeSerializer


class NestedPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            "uuid",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
        }


class PlanSerializer(URNModelSerializer, serializers.ModelSerializer):
    plantype = PlanTypeSerializer(
        required=False,
        read_only=True,
        help_text=get_help_text("plannen.PlanType", "type"),
    )
    plantype_uuid = UUIDRelatedField(
        queryset=PlanType.objects.all(),
        write_only=True,
        source="plantype",
        help_text=_("UUID van de gekoppelde plantype."),
    )

    class Meta:
        model = Plan
        fields = [
            "urn",
            "uuid",
            "plantype",
            "plantype_uuid",
            "zaak",
            "domeinregister",
            "medewerker",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
            "urn": {
                "lookup_field": "uuid",
                "help_text": _("De Uniform Resource Name van de externe taak."),
            },
        }
