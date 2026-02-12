from django.contrib import admin

from ..models.doel import Doel


@admin.register(Doel)
class DoelAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "titel",
        "persoon",
        "doeltype",
        "status",
        "hoofd_doel",
        "startdatum",
    )
    list_filter = (
        "doeltype",
        "status",
    )
    search_fields = (
        "uuid",
        "titel",
    )
    readonly_fields = ("uuid",)
    filter_horizontal = ("plannen",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uuid",
                    "titel",
                    "doeltype",
                    "plannen",
                    "persoon",
                    "hoofd_doel",
                    "status",
                    "beschrijving",
                ),
            },
        ),
        (
            "Data",
            {
                "fields": ("startdatum", "einddatum"),
            },
        ),
        (
            "Voortgang",
            {
                "fields": ("resultaat", "toelichting_resultaat"),
            },
        ),
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("persoon", "doeltype", "hoofd_doel")
            .prefetch_related("plannen")
        )
