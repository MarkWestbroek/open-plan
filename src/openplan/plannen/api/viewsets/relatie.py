from django.db import transaction

import structlog
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from openplan.plannen.api.filtersets.relatie import RelatieFilter
from openplan.plannen.models.relatie import Relatie

from ...metrics import (
    relaties_create_counter,
    relaties_delete_counter,
    relaties_update_counter,
)
from ..serializers.relatie import RelatieSerializer

logger = structlog.stdlib.get_logger(__name__)


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
    filterset_class = RelatieFilter
    lookup_field = "uuid"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        relatie = serializer.instance
        logger.info(
            "relatie_created",
            uuid=str(relatie.uuid),
        )
        relaties_create_counter.add(1)

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        relatie = serializer.instance
        logger.info(
            "relatie_updated",
            uuid=str(relatie.uuid),
        )
        relaties_update_counter.add(1)

    @transaction.atomic
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        logger.info(
            "relatie_deleted",
            uuid=str(instance.uuid),
        )
        relaties_delete_counter.add(1)
