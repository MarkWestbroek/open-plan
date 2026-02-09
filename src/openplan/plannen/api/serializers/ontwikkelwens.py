from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.utils import get_help_text

from openplan.plannen.models.doel import Doel
from openplan.plannen.models.doelcategorie import DoelCategorie
from openplan.plannen.models.ontwikkelwens import Ontwikkelwens
from openplan.utils.fields import UUIDRelatedField

from .doel import NestedDoelSerializer
from .doelcategorie import DoelCategorieSerializer


class OntwikkelwensSerializer(serializers.ModelSerializer):
    doel = NestedDoelSerializer(
        read_only=True,
        help_text=get_help_text("plannen.Doel", "uuid"),
    )
    doel_categorieen = DoelCategorieSerializer(
        many=True,
        read_only=True,
        help_text=get_help_text("plannen.DoelCategorie", "uuid"),
    )

    doel_uuid = UUIDRelatedField(
        queryset=Doel.objects.all(),
        write_only=True,
        source="doel",
        help_text=_("UUID van het doel waaraan deze ontwikkelwens gekoppeld is."),
    )
    doel_categorieen_uuids = UUIDRelatedField(
        queryset=DoelCategorie.objects.all(),
        many=True,
        write_only=True,
        source="doel_categorieen",
        help_text=_(
            "UUIDs van de doelcategorieën waaraan deze ontwikkelwens gekoppeld is."
        ),
    )

    class Meta:
        model = Ontwikkelwens
        fields = [
            "uuid",
            "titel",
            "beschrijving",
            "status",
            "startdatum",
            "einddatum",
            "resultaat",
            "doel",
            "doel_uuid",
            "doel_categorieen",
            "doel_categorieen_uuids",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
        }
