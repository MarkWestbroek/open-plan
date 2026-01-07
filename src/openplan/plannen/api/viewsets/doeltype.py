from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from openplan.plannen.models.doeltype import DoelType

from ..serializers.doeltype import DoelTypeSerializer


@extend_schema(tags=["Doeltype"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle doeltypen opvragen.",
        description="Deze lijst kan gefilterd wordt met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek doeltype opvragen.",
        description="Een specifiek doeltype opvragen via UUID.",
    ),
    create=extend_schema(
        summary="Nieuw doeltype aanmaken.",
        description="Voeg een nieuw doeltype toe aan het systeem.",
    ),
    update=extend_schema(
        summary="Doeltype volledig bijwerken.",
        description="Werk alle gegevens van een doeltype bij.",
    ),
    partial_update=extend_schema(
        summary="Doeltype gedeeltelijk bijwerken.",
        description="Werk enkele gegevens van een doeltype bij.",
    ),
    destroy=extend_schema(
        summary="Doeltype verwijderen.",
        description="Verwijder een specifiek doeltype.",
    ),
)
class DoelTypeViewSet(viewsets.ModelViewSet):
    queryset = DoelType.objects.all()
    serializer_class = DoelTypeSerializer
    filterset_fields = {
        "type",
    }
    lookup_field = "uuid"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
