from django.contrib import admin

from ..models.plan import Plan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "plantype",
    )
    list_filter = ("plantype",)
    search_fields = ("uuid", "plantype__naam")
    ordering = ("-uuid",)
    readonly_fields = ("uuid",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uuid",
                    "plantype",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("plantype")
