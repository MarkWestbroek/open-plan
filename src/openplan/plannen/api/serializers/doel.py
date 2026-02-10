from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from openplan.plannen.models.doel import Doel
from openplan.plannen.models.doeltype import DoelType
from openplan.plannen.models.persoon import Persoon
from openplan.plannen.models.plan import Plan
from openplan.plannen.models.validators import validate_primary_persoon
from openplan.utils.fields import UUIDRelatedField

from .doeltype import NestedDoelTypeSerializer
from .persoon import PersoonSerializer
from .plan import NestedPlanSerializer


class NestedDoelSerializer(serializers.ModelSerializer):
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
            "status",
            "titel",
            "beschrijving",
            "startdatum",
            "einddatum",
            "resultaat",
            "toelichting_resultaat",
            "hoofd_doel",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
        }


class DoelSerializer(serializers.ModelSerializer):
    doeltype = NestedDoelTypeSerializer(
        read_only=True,
    )
    plannen = NestedPlanSerializer(
        many=True,
        read_only=True,
    )
    persoon = PersoonSerializer(
        read_only=True,
    )

    doeltype_uuid = UUIDRelatedField(
        queryset=DoelType.objects.all(),
        write_only=True,
        source="doeltype",
        help_text=_("UUID van de gekoppelde doeltype."),
    )
    plannen_uuids = UUIDRelatedField(
        queryset=Plan.objects.all(),
        many=True,
        write_only=True,
        source="plannen",
        help_text=_("UUID van de plannen waaraan dit doel gekoppelt is."),
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
            "plannen",
            "plannen_uuids",
            "doeltype",
            "doeltype_uuid",
            "persoon",
            "persoon_uuid",
            "status",
            "titel",
            "beschrijving",
            "startdatum",
            "einddatum",
            "resultaat",
            "toelichting_resultaat",
            "hoofd_doel",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
        }

    def validate(self, attrs):
        persoon = attrs.get("persoon")

        if persoon is None and self.instance:
            persoon = self.instance.persoon

        if persoon:
            try:
                validate_primary_persoon(persoon)
            except ValidationError as exc:
                raise serializers.ValidationError(exc.message_dict)

        return attrs
