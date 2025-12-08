from django.contrib import admin

from ..models.relatie import Relatie


@admin.register(Relatie)
class RelatieAdmin(admin.ModelAdmin):
    list_display = (
        "persoon",
        "relatietype",
        "gerelateerde_persoon",
    )
    list_filter = ("relatietype",)
    search_fields = (
        "persoon__naam",
        "gerelateerde_persoon__naam",
        "relatietype__naam",
        "uuid",
    )
    readonly_fields = ("uuid",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uuid",
                    "persoon",
                    "gerelateerde_persoon",
                    "relatietype",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("persoon", "gerelateerde_persoon", "relatietype")
        )
