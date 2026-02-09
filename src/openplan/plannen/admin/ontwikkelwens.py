from django.contrib import admin

from ..models.ontwikkelwens import Ontwikkelwens


@admin.register(Ontwikkelwens)
class OntwikkelwensAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "titel",
        "doel",
        "status",
        "startdatum",
    )
    list_filter = (
        "doel_categorieen",
        "status",
    )
    search_fields = (
        "uuid",
        "titel",
    )
    ordering = ("-pk",)
    readonly_fields = ("uuid",)
    filter_horizontal = ("doel_categorieen",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uuid",
                    "titel",
                    "doel",
                    "doel_categorieen",
                    "status",
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
            "Beschrijving",
            {
                "fields": ("beschrijving",),
            },
        ),
        (
            "Resultaat",
            {
                "fields": ("resultaat",),
            },
        ),
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("doel")
            .prefetch_related("doel_categorieen")
        )
