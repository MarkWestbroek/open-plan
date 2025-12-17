from django.contrib import admin

from ..models.contactmoment import Contactmoment


@admin.register(Contactmoment)
class ContactmomentAdmin(admin.ModelAdmin):
    list_display = (
        "plan",
        "uuid",
    )
    list_filter = ("plan",)
    # search_fields = ("plan", "uuid")
    ordering = ("plan",)
    readonly_fields = ("uuid",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uuid",
                    "plan",
                ),
            },
        ),
    )
