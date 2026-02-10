from django.db import transaction

import structlog
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from openplan.plannen.api.serializers.ontwikkelwens import OntwikkelwensSerializer
from openplan.plannen.models.ontwikkelwens import Ontwikkelwens

logger = structlog.stdlib.get_logger(__name__)


@extend_schema(tags=["Ontwikkelwens"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle ontwikkelwensen opvragen.",
        description="Deze lijst kan gefilterd worden met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifieke ontwikkelwens opvragen.",
        description="Een specifieke ontwikkelwens opvragen via UUID.",
    ),
    create=extend_schema(
        summary="Nieuwe ontwikkelwens aanmaken.",
        description="Voeg een nieuwe ontwikkelwens toe aan het systeem.",
    ),
    update=extend_schema(
        summary="Ontwikkelwens volledig bijwerken.",
        description="Werk alle gegevens van een ontwikkelwens bij.",
    ),
    partial_update=extend_schema(
        summary="Ontwikkelwens gedeeltelijk bijwerken.",
        description="Werk enkele gegevens van een ontwikkelwens bij.",
    ),
    destroy=extend_schema(
        summary="Ontwikkelwens verwijderen.",
        description="Verwijder een specifieke ontwikkelwens.",
    ),
)
class OntwikkelwensViewSet(viewsets.ModelViewSet):
    queryset = Ontwikkelwens.objects.all()
    serializer_class = OntwikkelwensSerializer
    lookup_field = "uuid"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        ontwikkelwens = serializer.instance
        logger.info(
            "ontwikkelwens_created",
            uuid=str(ontwikkelwens.uuid),
            doel_uuid=str(ontwikkelwens.doel.uuid),
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        ontwikkelwens = serializer.instance
        logger.info(
            "ontwikkelwens_updated",
            uuid=str(ontwikkelwens.uuid),
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        logger.info(
            "ontwikkelwens_deleted",
            uuid=str(instance.uuid),
        )
