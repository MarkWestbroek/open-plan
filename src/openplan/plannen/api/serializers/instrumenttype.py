from rest_framework import serializers

from openplan.plannen.models.instrumenttype import InstrumentType


class InstrumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentType
        fields = ["uuid", "type"]

        extra_kwargs = {
            "uuid": {"read_only": True},
        }
