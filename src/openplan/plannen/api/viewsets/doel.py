from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from openplan.plannen.models.doel import Doel

from ..filtersets.doel import DoelFilter
from ..serializers.doel import DoelSerializer


@extend_schema(tags=["Doel"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle doelen opvragen.",
        description="Deze lijst kan gefilterd wordt met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek doel opvragen.",
        description="Een specifiek doel opvragen via UUID.",
    ),
    create=extend_schema(
        summary="Nieuw doel aanmaken.",
        description="Voeg een nieuw doel toe aan het systeem.",
    ),
    update=extend_schema(
        summary="Doel volledig bijwerken.",
        description="Werk alle gegevens van een doel bij.",
    ),
    partial_update=extend_schema(
        summary="Doel gedeeltelijk bijwerken.",
        description="Werk enkele gegevens van een doel bij.",
    ),
    destroy=extend_schema(
        summary="Doel verwijderen.",
        description="Verwijder een specifiek doel.",
    ),
)
class DoelViewSet(viewsets.ModelViewSet):
    queryset = Doel.objects.all()
    serializer_class = DoelSerializer
    filterset_class = DoelFilter
    lookup_field = "uuid"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
