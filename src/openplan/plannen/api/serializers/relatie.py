from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from openplan.plannen.models.persoon import Persoon
from openplan.plannen.models.relatie import Relatie
from openplan.plannen.models.relatietype import RelatieType
from openplan.utils.fields import UUIDRelatedField

from .persoon import PersoonSerializer
from .relatietype import RelatieTypeSerializer


class RelatieSerializer(serializers.ModelSerializer):
    persoon = PersoonSerializer(
        read_only=True,
    )
    gerelateerde_persoon = PersoonSerializer(
        read_only=True,
    )
    relatietype = RelatieTypeSerializer(
        read_only=True,
    )

    persoon_uuid = UUIDRelatedField(
        queryset=Persoon.objects.all(),
        write_only=True,
        source="persoon",
        help_text=_("UUID van de primaire persoon."),
    )
    gerelateerde_persoon_uuid = UUIDRelatedField(
        queryset=Persoon.objects.all(),
        write_only=True,
        source="gerelateerde_persoon",
        help_text=_("UUID van de gerelateerde persoon."),
    )
    relatietype_uuid = UUIDRelatedField(
        queryset=RelatieType.objects.all(),
        write_only=True,
        source="relatietype",
        help_text=_("UUID van het relatietype."),
    )

    class Meta:
        model = Relatie
        fields = [
            "uuid",
            "persoon",
            "persoon_uuid",
            "gerelateerde_persoon",
            "gerelateerde_persoon_uuid",
            "relatietype",
            "relatietype_uuid",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
        }

    def validate(self, attrs):
        instance = self.instance or Relatie()
        for attr, value in attrs.items():
            setattr(instance, attr, value)

        instance.clean()
        return attrs
