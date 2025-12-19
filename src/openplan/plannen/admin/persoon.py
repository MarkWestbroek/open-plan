from django.contrib import admin

from ..models.persoon import Persoon


@admin.register(Persoon)
class PersoonAdmin(admin.ModelAdmin):
    list_display = ("uuid",)
    search_fields = ("uuid",)
    readonly_fields = ("uuid",)

    fieldsets = (
        (
            None,
            {
                "fields": ("uuid",),
            },
        ),
        (
            "URLs",
            {
                "fields": (
                    "persoonsprofiel",
                    "klant",
                    "bsn",
                ),
            },
        ),
    )
