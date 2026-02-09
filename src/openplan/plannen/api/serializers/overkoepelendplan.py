from rest_framework import serializers

from openplan.utils.serializers import URNModelSerializer

from ...models.overkoepelendplan import OverkoepelendPlan


class OverkoepelendPlanSerializer(URNModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = OverkoepelendPlan
        fields = [
            "urn",
            "uuid",
            "titel",
            "status",
            "medewerker",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
        }
