from django.contrib import admin

from ..models.contactmoment import Contactmoment


@admin.register(Contactmoment)
class ContactmomentAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "plan",
        "status",
        "datum",
    )
    list_filter = (
        "plan",
        "status",
    )
    search_fields = ("uuid",)
    ordering = (
        "plan",
        "-datum",
    )
    readonly_fields = ("uuid",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uuid",
                    "plan",
                    "status",
                    "datum",
                ),
            },
        ),
        (
            "Beschrijving",
            {
                "fields": (
                    "toelichting_status",
                    "notitie",
                ),
            },
        ),
        (
            "Relatie",
            {
                "fields": ("persoonsprofiel",),
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("plan")
