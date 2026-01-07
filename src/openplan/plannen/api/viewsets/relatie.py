from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from openplan.plannen.models.relatie import Relatie

from ..serializers.relatie import RelatieSerializer


@extend_schema(tags=["Relatie"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle relaties opvragen.",
        description="Deze lijst kan gefilterd wordt met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek relatie opvragen.",
        description="Een specifiek relatie opvragen via UUID.",
    ),
    create=extend_schema(
        summary="Nieuw relatie aanmaken.",
        description="Voeg een nieuw relatie toe aan het systeem.",
    ),
    update=extend_schema(
        summary="Relatie volledig bijwerken.",
        description="Werk alle gegevens van een relatie bij.",
    ),
    partial_update=extend_schema(
        summary="Relatie gedeeltelijk bijwerken.",
        description="Werk enkele gegevens van een relatie bij.",
    ),
    destroy=extend_schema(
        summary="Relatie verwijderen.",
        description="Verwijder een specifiek relatie.",
    ),
)
class RelatieViewSet(viewsets.ModelViewSet):
    queryset = Relatie.objects.all()
    serializer_class = RelatieSerializer
    lookup_field = "uuid"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
