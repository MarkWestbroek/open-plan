from rest_framework import serializers

from openplan.plannen.api.serializers.relatietype import RelatieTypeSerializer
from openplan.plannen.models.persoon import Persoon
from openplan.plannen.models.relatie import Relatie


class VersionGerelateerdePersoonSerializer(serializers.ModelSerializer):
    relatietype = RelatieTypeSerializer(read_only=True)
    gerelateerde_persoon_uuid = serializers.UUIDField(
        source="gerelateerde_persoon.uuid", read_only=True
    )

    class Meta:
        model = Relatie
        fields = ["uuid", "gerelateerde_persoon_uuid", "relatietype"]


class VersionPersoonSerializer(serializers.ModelSerializer):
    relaties_vanuit = VersionGerelateerdePersoonSerializer(many=True, read_only=True)

    class Meta:
        model = Persoon
        fields = [
            "uuid",
            "persoonsprofiel_url",
            "open_klant_url",
            "bsn",
            "relaties_vanuit",
        ]

    def to_representation(self, instance):
        # get default serialized data
        data = super().to_representation(instance)
        # explicitly reorder fields
        ordered_data = {
            "uuid": data["uuid"],
            "persoonsprofiel_url": data["persoonsprofiel_url"],
            "open_klant_url": data["open_klant_url"],
            "bsn": data["bsn"],
            "relaties_vanuit": data["relaties_vanuit"],
        }
        return ordered_data


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
