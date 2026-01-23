import structlog
from drf_spectacular.utils import extend_schema, extend_schema_view
from pghistory.models import Events
from rest_framework import viewsets

from ..serializers.history import HistoryEventSerializer

logger = structlog.stdlib.get_logger(__name__)


@extend_schema(tags=["History"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle history opvragen.",
        description="Deze lijst kan gefilterd wordt met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek history opvragen.",
        description="Een specifiek history opvragen via UUID.",
    ),
)
class HistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Events.objects.all()
    serializer_class = HistoryEventSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        if "tracks" in self.request.query_params:
            qs = qs.tracks(self.request.query_params["tracks"])

        if "references" in self.request.query_params:
            qs = qs.references(self.request.query_params["references"])

        return qs
