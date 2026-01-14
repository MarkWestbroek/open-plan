from django.db import transaction

import structlog
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from openplan.plannen.models.instrumenttype import InstrumentType

from ...metrics import (
    instrumenttypen_create_counter,
    instrumenttypen_delete_counter,
    instrumenttypen_update_counter,
)
from ..serializers.instrumenttype import InstrumentTypeSerializer

logger = structlog.stdlib.get_logger(__name__)


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

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        instrumenttype = serializer.instance
        logger.info(
            "instrumenttype_created",
            uuid=str(instrumenttype.uuid),
        )
        instrumenttypen_create_counter.add(1)

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        instrumenttype = serializer.instance
        logger.info(
            "instrumenttype_updated",
            uuid=str(instrumenttype.uuid),
        )
        instrumenttypen_update_counter.add(1)

    @transaction.atomic
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        logger.info(
            "instrumenttype_deleted",
            uuid=str(instance.uuid),
        )
        instrumenttypen_delete_counter.add(1)
