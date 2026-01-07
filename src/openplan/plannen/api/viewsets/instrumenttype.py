from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from openplan.plannen.models.instrumenttype import InstrumentType

from ..serializers.instrumenttype import InstrumentTypeSerializer


@extend_schema(tags=["Instrumenttype"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle instrumenttypen opvragen.",
        description="Deze lijst kan gefilterd wordt met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek instrumenttype opvragen.",
        description="Een specifiek instrumenttype opvragen via UUID.",
    ),
    create=extend_schema(
        summary="Nieuw instrumenttype aanmaken.",
        description="Voeg een nieuw instrumenttype toe aan het systeem.",
    ),
    update=extend_schema(
        summary="Instrumenttypen volledig bijwerken.",
        description="Werk alle gegevens van een instrumenttype bij.",
    ),
    partial_update=extend_schema(
        summary="Instrumenttypen gedeeltelijk bijwerken.",
        description="Werk enkele gegevens van een instrumenttype bij.",
    ),
    destroy=extend_schema(
        summary="Instrumenttypen verwijderen.",
        description="Verwijder een specifiek instrumenttype.",
    ),
)
class InstrumentTypeViewSet(viewsets.ModelViewSet):
    queryset = InstrumentType.objects.all()
    serializer_class = InstrumentTypeSerializer
    lookup_field = "uuid"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
