from django.contrib import admin

from ..models.overkoepelendplan import OverkoepelendPlan


@admin.register(OverkoepelendPlan)
class OverkoepelendPlanAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "titel",
        "status",
    )
    search_fields = ("uuid", "titel")
    readonly_fields = ("uuid",)

    fieldsets = (
        (
            None,
            {
                "fields": ("uuid", "titel", "status", "medewerker"),
            },
        ),
    )
