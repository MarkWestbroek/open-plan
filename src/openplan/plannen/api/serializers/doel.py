from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openplan.plannen.models.doel import Doel
from openplan.plannen.models.doeltype import DoelType
from openplan.utils.fields import UUIDRelatedField

from .doeltype import DoelTypeSerializer


class DoelSerializer(serializers.ModelSerializer):
    doeltype = DoelTypeSerializer(
        required=False,
        read_only=True,
        help_text=get_help_text("plannen.DoelType", "type"),
    )
    doeltype_uuid = UUIDRelatedField(
        queryset=DoelType.objects.all(),
        write_only=True,
        source="doeltype",
        help_text=_("UUID van de gekoppelde doeltype."),
    )

    class Meta:
        model = Doel
        fields = ["uuid", "doeltype", "doeltype_uuid"]
        extra_kwargs = {
            "uuid": {"read_only": True},
        }
