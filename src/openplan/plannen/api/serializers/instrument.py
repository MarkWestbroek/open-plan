from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from openplan.plannen.models.doel import Doel
from openplan.plannen.models.instrument import Instrument
from openplan.plannen.models.instrumenttype import InstrumentType
from openplan.plannen.models.ontwikkelwens import Ontwikkelwens
from openplan.utils.fields import UUIDRelatedField

from .doel import NestedDoelSerializer
from .instrumentcategorie import InstrumentCategorieSerializer
from .instrumenttype import NestedInstrumentTypeSerializer


class InstrumentSerializer(serializers.ModelSerializer):
    doelen = NestedDoelSerializer(
        many=True,
        read_only=True,
    )
    ontwikkelwensen = NestedDoelSerializer(
        many=True,
        read_only=True,
    )
    instrumenttype = NestedInstrumentTypeSerializer(
        read_only=True,
    )
    instrument_categorieen = InstrumentCategorieSerializer(
        many=True,
        read_only=True,
    )

    doelen_uuids = UUIDRelatedField(
        queryset=Doel.objects.all(),
        many=True,
        write_only=True,
        source="doelen",
        help_text=_("UUID's van het doel waaraan dit instrument gekoppeld is."),
    )
    ontwikkelwensen_uuids = UUIDRelatedField(
        queryset=Ontwikkelwens.objects.all(),
        many=True,
        write_only=True,
        source="ontwikkelwensen",
        help_text=_(
            "UUID's van het ontwikkelwens waaraan dit instrument gekoppeld is."
        ),
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
            "titel",
            "startdatum",
            "einddatum",
            "status",
            "product",
            "zaak",
            "resultaat",
            "doelen",
            "doelen_uuids",
            "ontwikkelwensen",
            "ontwikkelwensen_uuids",
            "instrumenttype",
            "instrumenttype_uuid",
            "instrument_categorieen",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
        }
