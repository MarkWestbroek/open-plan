import structlog
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from openplan.plannen.models.plantype import PlanType

from ..filtersets.plantype import PlanTypeFilter
from ..serializers.plantype import PlanTypeSerializer

logger = structlog.stdlib.get_logger(__name__)


@extend_schema(tags=["Plantype"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle plantypes opvragen.",
        description="Deze lijst kan gefilterd wordt met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek plantype opvragen.",
        description="Een specifiek plantype opvragen via UUID.",
    ),
    create=extend_schema(
        summary="Nieuw plantype aanmaken.",
        description="Voeg een nieuw plantype toe aan het systeem.",
    ),
    update=extend_schema(
        summary="Plantype volledig bijwerken.",
        description="Werk alle gegevens van een plantype bij.",
    ),
    partial_update=extend_schema(
        summary="Plantype gedeeltelijk bijwerken.",
        description="Werk enkele gegevens van een plantype bij.",
    ),
    destroy=extend_schema(
        summary="Plantype verwijderen.",
        description="Verwijder een specifiek plantype.",
    ),
)
class PlanTypeViewSet(viewsets.ModelViewSet):
    queryset = PlanType.objects.all()
    serializer_class = PlanTypeSerializer
    filterset_class = PlanTypeFilter
    lookup_field = "uuid"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
