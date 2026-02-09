from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openplan.plannen.models.overkoepelendplan import OverkoepelendPlan
from openplan.plannen.models.plan import Plan
from openplan.plannen.models.plantype import PlanType
from openplan.utils.fields import UUIDRelatedField
from openplan.utils.serializers import URNModelSerializer

from ..serializers.overkoepelendplan import OverkoepelendPlanSerializer
from .plantype import PlanTypeSerializer


class NestedPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            "uuid",
            "status",
            "titel",
            "notitie",
            "startdatum",
            "einddatum",
            "reden_einde",
            "zaak",
            "domeinregister",
            "medewerker",
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

    overkoepelend_plan = OverkoepelendPlanSerializer(
        required=False,
        read_only=True,
        help_text=get_help_text("plannen.OverkoepelendPlan", "titel"),
    )
    overkoepelend_plan_uuid = UUIDRelatedField(
        queryset=OverkoepelendPlan.objects.all(),
        write_only=True,
        source="overkoepelend_plan",
        help_text=_("UUID van het overkoepelend plan."),
    )

    class Meta:
        model = Plan
        fields = [
            "urn",
            "uuid",
            "status",
            "titel",
            "notitie",
            "startdatum",
            "einddatum",
            "reden_einde",
            "plantype",
            "plantype_uuid",
            "overkoepelend_plan",
            "overkoepelend_plan_uuid",
            "zaak",
            "domeinregister",
            "medewerker",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
            "urn": {
                "lookup_field": "uuid",
                "help_text": _("De Uniform Resource Name van de plan."),
            },
        }
