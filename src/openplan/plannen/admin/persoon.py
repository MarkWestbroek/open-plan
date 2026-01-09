from django.contrib import admin

from ..models.persoon import Persoon


@admin.register(Persoon)
class PersoonAdmin(admin.ModelAdmin):
    list_display = ("uuid",)
    search_fields = ("uuid",)
    readonly_fields = ("uuid",)

    fields = [
        "uuid",
        "persoonsprofiel_url",
        "open_klant_url",
        "bsn",
    ]
