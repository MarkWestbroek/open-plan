from django.db import transaction

import structlog
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from openplan.plannen.models.relatietype import RelatieType

from ..serializers.relatietype import RelatieTypeSerializer

logger = structlog.stdlib.get_logger(__name__)


@extend_schema(tags=["Relatietype"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle relatietypes opvragen.",
        description="Deze lijst kan gefilterd wordt met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek relatietype opvragen.",
        description="Een specifiek relatietype opvragen via UUID.",
    ),
    create=extend_schema(
        summary="Nieuw relatietype aanmaken.",
        description="Voeg een nieuw relatietype toe aan het systeem.",
    ),
    update=extend_schema(
        summary="Relatietype volledig bijwerken.",
        description="Werk alle gegevens van een relatietype bij.",
    ),
    partial_update=extend_schema(
        summary="Relatietype gedeeltelijk bijwerken.",
        description="Werk enkele gegevens van een relatietype bij.",
    ),
    destroy=extend_schema(
        summary="Relatietype verwijderen.",
        description="Verwijder een specifiek relatietype.",
    ),
)
class RelatieTypeViewSet(viewsets.ModelViewSet):
    queryset = RelatieType.objects.all()
    serializer_class = RelatieTypeSerializer
    filterset_fields = {
        "naam",
    }
    lookup_field = "uuid"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        relatietype = serializer.instance
        logger.info(
            "relatietype_created",
            uuid=str(relatietype.uuid),
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        relatietype = serializer.instance
        logger.info(
            "relatietype_updated",
            uuid=str(relatietype.uuid),
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        logger.info(
            "relatietype_deleted",
            uuid=str(instance.uuid),
        )
