from rest_framework import serializers

from openplan.plannen.models.doelcategorie import DoelCategorie


class DoelCategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoelCategorie
        fields = ["uuid", "naam"]

        extra_kwargs = {
            "uuid": {"read_only": True},
        }
