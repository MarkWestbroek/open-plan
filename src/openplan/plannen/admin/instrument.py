from django.contrib import admin

from ..models.instrument import Instrument


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "titel",
        "instrumenttype",
        "status",
        "startdatum",
    )
    list_filter = (
        "instrumenttype",
        "instrument_categorieen",
        "status",
    )
    search_fields = (
        "uuid",
        "titel",
    )
    ordering = ("-pk",)
    readonly_fields = ("uuid",)
    filter_horizontal = (
        "doelen",
        "ontwikkelwensen",
        "instrument_categorieen",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uuid",
                    "titel",
                    "instrumenttype",
                    "status",
                ),
            },
        ),
        (
            "Relaties",
            {
                "fields": (
                    "doelen",
                    "ontwikkelwensen",
                    "instrument_categorieen",
                ),
            },
        ),
        (
            "Data",
            {
                "fields": (
                    "startdatum",
                    "einddatum",
                ),
            },
        ),
        (
            "Resultaat",
            {
                "fields": ("resultaat",),
            },
        ),
        (
            "URNs",
            {
                "fields": (
                    "product",
                    "zaak",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("instrumenttype")
            .prefetch_related(
                "doelen",
                "ontwikkelwensen",
                "instrument_categorieen",
            )
        )
