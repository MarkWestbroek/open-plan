from django.contrib import admin

from ..models.instrument import Instrument


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ("uuid", "doel", "instrumenttype")
    search_fields = ("uuid",)
    readonly_fields = ("uuid",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uuid",
                    "doel",
                    "instrumenttype",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("doel", "instrumenttype")
