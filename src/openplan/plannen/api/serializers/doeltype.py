from rest_framework import serializers

from openplan.plannen.models.doeltype import DoelType


class DoelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoelType
        fields = ["uuid", "type"]

        extra_kwargs = {
            "uuid": {"read_only": True},
        }
