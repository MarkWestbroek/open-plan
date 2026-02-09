from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openplan.plannen.api.serializers.doelcategorie import DoelCategorieSerializer
from openplan.plannen.models.doelcategorie import DoelCategorie
from openplan.plannen.models.doeltype import DoelType
from openplan.utils.fields import UUIDRelatedField


class NestedDoelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoelType
        fields = ["uuid", "doel_type"]

        extra_kwargs = {
            "uuid": {"read_only": True},
        }


class DoelTypeSerializer(serializers.ModelSerializer):
    categorieen = DoelCategorieSerializer(
        many=True,
        read_only=True,
        help_text=get_help_text("plannen.DoelCategorie", "uuid"),
    )

    categorieen_uuids = UUIDRelatedField(
        queryset=DoelCategorie.objects.all(),
        many=True,
        write_only=True,
        source="categorieen",
        help_text=_("UUID's van de doelcategorieen waaraan dit doeltype gekoppeld is."),
    )

    class Meta:
        model = DoelType
        fields = ["uuid", "doel_type", "categorieen", "categorieen_uuids"]

        extra_kwargs = {
            "uuid": {"read_only": True},
        }
