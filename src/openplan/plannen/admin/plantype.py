from django.contrib import admin

from ..models.plantype import PlanType


@admin.register(PlanType)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        "type",
        "uuid",
    )
    list_filter = ("type",)
    search_fields = ("type", "uuid")
    ordering = ("type",)
    readonly_fields = ("uuid",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uuid",
                    "type",
                ),
            },
        ),
    )
