from rest_framework import serializers

from openplan.plannen.models.plantype import PlanType


class PlanTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanType
        fields = ["uuid", "type"]

        extra_kwargs = {
            "uuid": {"read_only": True},
        }
