from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openplan.plannen.models.contactmoment import Contactmoment
from openplan.plannen.models.plan import Plan
from openplan.utils.fields import UUIDRelatedField

from .plan import PlanSerializer


class ContactmomentSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(
        read_only=True,
        help_text=get_help_text("plannen.Plan", "uuid"),
    )

    plan_uuid = UUIDRelatedField(
        queryset=Plan.objects.all(),
        write_only=True,
        source="plan",
        help_text=_("UUID van het plan waarbij dit contactmoment hoort."),
    )

    class Meta:
        model = Contactmoment
        fields = [
            "uuid",
            "plan",
            "plan_uuid",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
        }
