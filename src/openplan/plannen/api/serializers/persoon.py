from rest_framework import serializers

from openplan.plannen.models.persoon import Persoon


class PersoonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persoon
        fields = [
            "uuid",
            "persoonsprofiel_url",
            "open_klant_url",
            "bsn",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
        }
