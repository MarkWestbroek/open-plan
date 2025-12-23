from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openplan.plannen.models.doel import Doel
from openplan.plannen.models.instrument import Instrument
from openplan.plannen.models.instrumenttype import InstrumentType
from openplan.utils.fields import UUIDRelatedField

from .doel import NestedDoelSerializer
from .instrumenttype import InstrumentTypeSerializer


class InstrumentSerializer(serializers.ModelSerializer):
    doel = NestedDoelSerializer(
        read_only=True,
        help_text=get_help_text("plannen.Doel", "uuid"),
    )
    instrumenttype = InstrumentTypeSerializer(
        read_only=True,
        help_text=get_help_text("plannen.Instrumenttype", "type"),
    )

    doel_uuid = UUIDRelatedField(
        queryset=Doel.objects.all(),
        write_only=True,
        source="doel",
        help_text=_("UUID van het doel waaraan dit instrument gekoppeld is."),
    )
    instrumenttype_uuid = UUIDRelatedField(
        queryset=InstrumentType.objects.all(),
        write_only=True,
        source="instrumenttype",
        help_text=_("UUID van het type instrument dat hier wordt toegepast."),
    )

    class Meta:
        model = Instrument
        fields = [
            "uuid",
            "doel",
            "doel_uuid",
            "instrumenttype",
            "instrumenttype_uuid",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
        }
