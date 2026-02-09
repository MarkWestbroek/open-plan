from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openplan.plannen.models.instrumentcategorie import InstrumentCategorie
from openplan.plannen.models.instrumenttype import InstrumentType
from openplan.utils.fields import UUIDRelatedField

from .instrumentcategorie import InstrumentCategorieSerializer


class NestedInstrumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentType
        fields = ["uuid", "instrument_type"]

        extra_kwargs = {
            "uuid": {"read_only": True},
        }


class InstrumentTypeSerializer(serializers.ModelSerializer):
    categorieen = InstrumentCategorieSerializer(
        many=True,
        read_only=True,
        help_text=get_help_text("plannen.InstrumentCategorie", "uuid"),
    )

    categorieen_uuids = UUIDRelatedField(
        queryset=InstrumentCategorie.objects.all(),
        many=True,
        write_only=True,
        source="categorieen",
        help_text=_(
            "UUID's van de instrumentcategorieen waaraan dit instrument gekoppeld is."
        ),
    )

    class Meta:
        model = InstrumentType
        fields = ["uuid", "instrument_type", "categorieen", "categorieen_uuids"]

        extra_kwargs = {
            "uuid": {"read_only": True},
        }
