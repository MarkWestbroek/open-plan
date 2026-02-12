from django.contrib import admin

from ..models.plan import Plan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "titel",
        "overkoepelend_plan",
        "plantype",
        "status",
        "startdatum",
    )

    list_filter = (
        "plantype",
        "status",
    )

    search_fields = (
        "uuid",
        "titel",
    )

    readonly_fields = ("uuid",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uuid",
                    "titel",
                    "plantype",
                    "overkoepelend_plan",
                    "status",
                    "fase",
                    "notitie",
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
            "Beëindiging",
            {
                "fields": ("reden_einde",),
            },
        ),
        (
            "URNs",
            {
                "fields": (
                    "zaak",
                    "domeinregister",
                    "medewerker",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "plantype",
                "overkoepelend_plan",
            )
        )
