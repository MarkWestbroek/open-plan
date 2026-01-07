from django.db import transaction

import structlog
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from openplan.plannen.models.doelcategorie import DoelCategorie

from ..serializers.doelcategorie import DoelCategorieSerializer

logger = structlog.stdlib.get_logger(__name__)


@extend_schema(tags=["Doelcategorie"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle doelcategorieën opvragen.",
        description="Deze lijst kan gefilterd wordt met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek doelcategorie opvragen.",
        description="Een specifiek doelcategorie opvragen via UUID.",
    ),
    create=extend_schema(
        summary="Nieuw doelcategorie aanmaken.",
        description="Voeg een nieuw doelcategorie toe aan het systeem.",
    ),
    update=extend_schema(
        summary="Doelcategorie volledig bijwerken.",
        description="Werk alle gegevens van een doelcategorie bij.",
    ),
    partial_update=extend_schema(
        summary="Doelcategorie gedeeltelijk bijwerken.",
        description="Werk enkele gegevens van een doelcategorie bij.",
    ),
    destroy=extend_schema(
        summary="Doelcategorie verwijderen.",
        description="Verwijder een specifiek doelcategorie.",
    ),
)
class DoelCategorieViewSet(viewsets.ModelViewSet):
    queryset = DoelCategorie.objects.all()
    serializer_class = DoelCategorieSerializer
    filterset_fields = {
        "naam",
    }
    lookup_field = "uuid"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        doelcategorie = serializer.instance
        logger.info(
            "doelcategorie_created",
            uuid=str(doelcategorie.uuid),
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        doelcategorie = serializer.instance
        logger.info(
            "doelcategorie_updated",
            uuid=str(doelcategorie.uuid),
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        logger.info(
            "doelcategorie_deleted",
            uuid=str(instance.uuid),
        )
