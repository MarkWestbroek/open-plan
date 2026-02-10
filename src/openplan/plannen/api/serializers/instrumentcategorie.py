from rest_framework import serializers

from openplan.plannen.models.instrumentcategorie import InstrumentCategorie


class InstrumentCategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentCategorie
        fields = ["uuid", "naam"]

        extra_kwargs = {
            "uuid": {"read_only": True},
        }
