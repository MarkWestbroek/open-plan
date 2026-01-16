from django.db import transaction

import structlog
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from openplan.plannen.models.contactmoment import Contactmoment

from ...metrics import (
    contactmomenten_create_counter,
    contactmomenten_delete_counter,
    contactmomenten_update_counter,
)
from ..serializers.contactmoment import ContactmomentSerializer

logger = structlog.stdlib.get_logger(__name__)


@extend_schema(tags=["Contactmoment"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle contactmomenten opvragen.",
        description="Deze lijst kan gefilterd wordt met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek contactmoment opvragen.",
        description="Een specifiek contactmoment opvragen via UUID.",
    ),
    create=extend_schema(
        summary="Nieuw contactmoment aanmaken.",
        description="Voeg een nieuw contactmoment toe aan het systeem.",
    ),
    update=extend_schema(
        summary="Contactmoment volledig bijwerken.",
        description="Werk alle gegevens van een contactmoment bij.",
    ),
    partial_update=extend_schema(
        summary="Contactmoment gedeeltelijk bijwerken.",
        description="Werk enkele gegevens van een contactmoment bij.",
    ),
    destroy=extend_schema(
        summary="Contactmoment verwijderen.",
        description="Verwijder een specifiek contactmoment.",
    ),
)
class ContactmomentViewSet(viewsets.ModelViewSet):
    queryset = Contactmoment.objects.all()
    serializer_class = ContactmomentSerializer
    lookup_field = "uuid"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        contactmoment = serializer.instance
        logger.info(
            "contactmoment_created",
            uuid=str(contactmoment.uuid),
        )
        contactmomenten_create_counter.add(1)

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        contactmoment = serializer.instance
        logger.info(
            "contactmoment_updated",
            uuid=str(contactmoment.uuid),
        )
        contactmomenten_update_counter.add(1)

    @transaction.atomic
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        logger.info(
            "contactmoment_deleted",
            uuid=str(instance.uuid),
        )
        contactmomenten_delete_counter.add(1)
