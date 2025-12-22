from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openplan.plannen.models.doel import Doel
from openplan.plannen.models.doeltype import DoelType
from openplan.plannen.models.persoon import Persoon
from openplan.plannen.models.plan import Plan
from openplan.utils.fields import UUIDRelatedField

from .doeltype import DoelTypeSerializer
from .persoon import PersoonSerializer
from .plan import PlanSerializer


class DoelSerializer(serializers.ModelSerializer):
    doeltype = DoelTypeSerializer(
        read_only=True,
        help_text=get_help_text("plannen.DoelType", "type"),
    )
    plan = PlanSerializer(
        read_only=True,
        help_text=get_help_text("plannen.Plan", "uuid"),
    )
    persoon = PersoonSerializer(
        read_only=True,
        help_text=get_help_text("plannen.Persoon", "uuid"),
    )

    doeltype_uuid = UUIDRelatedField(
        queryset=DoelType.objects.all(),
        write_only=True,
        source="doeltype",
        help_text=_("UUID van de gekoppelde doeltype."),
    )
    plan_uuid = UUIDRelatedField(
        queryset=Plan.objects.all(),
        write_only=True,
        source="plan",
        help_text=_("UUID van het plan waarbij dit doel hoort."),
    )
    persoon_uuid = UUIDRelatedField(
        queryset=Persoon.objects.all(),
        write_only=True,
        source="persoon",
        help_text=_("UUID van de gekoppelde persoon."),
    )
    hoofd_doel = UUIDRelatedField(
        queryset=Doel.objects.all(),
        required=False,
        allow_null=True,
        help_text=_("UUID van de bovenliggende doel (optioneel)."),
    )

    class Meta:
        model = Doel
        fields = [
            "uuid",
            "plan",
            "plan_uuid",
            "doeltype",
            "doeltype_uuid",
            "persoon",
            "persoon_uuid",
            "hoofd_doel",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
        }

    def to_representation(self, instance):
        """Ensure hoofd_doel is serialized as a string UUID."""
        data = super().to_representation(instance)
        parent = instance.hoofd_doel
        data["hoofd_doel"] = str(parent.uuid) if parent else None
        return data
