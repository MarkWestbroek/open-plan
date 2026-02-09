from django.contrib import admin

from ..models.instrumenttype import InstrumentType


@admin.register(InstrumentType)
class InstrumentTypeAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "instrument_type",
    )
    list_filter = ("instrument_type",)
    search_fields = ("instrument_type", "uuid")
    ordering = ("instrument_type",)
    readonly_fields = ("uuid",)
    filter_horizontal = ("categorieen",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uuid",
                    "instrument_type",
                    "categorieen",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("categorieen")
