from django.contrib import admin

from ..models.relatietype import RelatieType


@admin.register(RelatieType)
class RelatieTypeAdmin(admin.ModelAdmin):
    list_display = (
        "naam",
        "uuid",
    )
    list_filter = ("naam",)
    search_fields = ("naam", "uuid")
    readonly_fields = ("uuid",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uuid",
                    "naam",
                ),
            },
        ),
    )
