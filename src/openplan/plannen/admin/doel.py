from django.contrib import admin

from ..models.doel import Doel


@admin.register(Doel)
class DoelAdmin(admin.ModelAdmin):
    list_display = (
        "plan",
        "persoon",
    )
    list_filter = ("plan",)
    search_fields = ("uuid", "persoon__naam", "plan__naam")
    ordering = ("-uuid",)
    readonly_fields = ("uuid",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uuid",
                    "doeltype",
                    "plan",
                    "persoon",
                    "hoofd_doel",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("plan", "persoon")
