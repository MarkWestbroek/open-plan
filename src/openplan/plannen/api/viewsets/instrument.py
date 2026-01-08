from django.db import transaction

import structlog
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from openplan.plannen.models.instrument import Instrument

from ..serializers.instrument import InstrumentSerializer

logger = structlog.stdlib.get_logger(__name__)


@extend_schema(tags=["Instrument"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle instrumenten opvragen.",
        description="Deze lijst kan gefilterd wordt met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek instrument opvragen.",
        description="Een specifiek instrument opvragen via UUID.",
    ),
    create=extend_schema(
        summary="Nieuw instrument aanmaken.",
        description="Voeg een nieuw instrument toe aan het systeem.",
    ),
    update=extend_schema(
        summary="Instrument volledig bijwerken.",
        description="Werk alle gegevens van een instrument bij.",
    ),
    partial_update=extend_schema(
        summary="Instrument gedeeltelijk bijwerken.",
        description="Werk enkele gegevens van een instrument bij.",
    ),
    destroy=extend_schema(
        summary="Instrument verwijderen.",
        description="Verwijder een specifiek instrument.",
    ),
)
class InstrumentViewSet(viewsets.ModelViewSet):
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerializer
    lookup_field = "uuid"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        instrument = serializer.instance
        logger.info(
            "instrument_created",
            uuid=str(instrument.uuid),
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        instrument = serializer.instance
        logger.info(
            "instrument_updated",
            uuid=str(instrument.uuid),
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        logger.info(
            "instrument_deleted",
            uuid=str(instance.uuid),
        )
