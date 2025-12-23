from rest_framework import serializers

from openplan.plannen.models.relatietype import RelatieType


class RelatieTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatieType
        fields = ["uuid", "naam"]

        extra_kwargs = {
            "uuid": {"read_only": True},
        }
