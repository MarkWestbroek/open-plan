from django.contrib import admin

from ..models.instrumentcategorie import InstrumentCategorie


@admin.register(InstrumentCategorie)
class InstrumentCategorieAdmin(admin.ModelAdmin):
    list_display = (
        "naam",
        "uuid",
    )
    list_filter = ("naam",)
    search_fields = ("naam", "uuid")
    ordering = ("naam",)
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
