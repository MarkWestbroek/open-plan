from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from openplan.plannen.models.persoon import Persoon

from ..serializers.persoon import PersoonSerializer


@extend_schema(tags=["Persoon"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle personen opvragen.",
        description="Deze lijst kan gefilterd wordt met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek persoon opvragen.",
        description="Een specifiek persoon opvragen via UUID.",
    ),
    create=extend_schema(
        summary="Nieuw persoon aanmaken.",
        description="Voeg een nieuw persoon toe aan het systeem.",
    ),
    update=extend_schema(
        summary="Persoon volledig bijwerken.",
        description="Werk alle gegevens van een persoon bij.",
    ),
    partial_update=extend_schema(
        summary="Persoon gedeeltelijk bijwerken.",
        description="Werk enkele gegevens van een persoon bij.",
    ),
    destroy=extend_schema(
        summary="Persoon verwijderen.",
        description="Verwijder een specifiek persoon.",
    ),
)
class PersoonViewSet(viewsets.ModelViewSet):
    queryset = Persoon.objects.all()
    serializer_class = PersoonSerializer
    lookup_field = "uuid"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
