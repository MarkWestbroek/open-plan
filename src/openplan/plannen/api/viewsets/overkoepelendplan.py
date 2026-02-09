from django.db import transaction

import structlog
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from openplan.plannen.api.serializers.overkoepelendplan import (
    OverkoepelendPlanSerializer,
)
from openplan.plannen.models.overkoepelendplan import OverkoepelendPlan

logger = structlog.stdlib.get_logger(__name__)


@extend_schema(tags=["Overkoepelend Plan"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle overkoepelende plannen opvragen.",
        description="Deze lijst kan gefilterd wordt met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek overkoepelend plan opvragen.",
        description="Een specifiek overkoepelend plan opvragen via UUID.",
    ),
    create=extend_schema(
        summary="Nieuw overkoepelend plan aanmaken.",
        description="Voeg een nieuw overkoepelend plan toe aan het systeem.",
    ),
    update=extend_schema(
        summary="Overkoepelend plan volledig bijwerken.",
        description="Werk alle gegevens van een overkoepelend plan bij.",
    ),
    partial_update=extend_schema(
        summary="Overkoepelend plan gedeeltelijk bijwerken.",
        description="Werk enkele gegevens van een overkoepelend plan bij.",
    ),
    destroy=extend_schema(
        summary="Overkoepelend plan verwijderen.",
        description="Verwijder een specifiek overkoepelend plan.",
    ),
)
class OverkoepelendPlanViewSet(viewsets.ModelViewSet):
    queryset = OverkoepelendPlan.objects.all()
    serializer_class = OverkoepelendPlanSerializer
    lookup_field = "uuid"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        plan = serializer.instance
        logger.info(
            "overkoepelendplan_created",
            uuid=str(plan.uuid),
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        plan = serializer.instance
        logger.info(
            "overkoepelendplan_updated",
            uuid=str(plan.uuid),
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        logger.info(
            "overkoepelendplan_deleted",
            uuid=str(instance.uuid),
        )
