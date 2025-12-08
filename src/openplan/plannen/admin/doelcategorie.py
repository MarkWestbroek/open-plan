from django.contrib import admin

from ..models.doelcategorie import DoelCategorie


@admin.register(DoelCategorie)
class DoelCategorieAdmin(admin.ModelAdmin):
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
