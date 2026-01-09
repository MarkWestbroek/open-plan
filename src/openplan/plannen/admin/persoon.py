from django.contrib import admin

from openplan.plannen.models.plan import Plan
from openplan.plannen.models.version import Version
from openplan.utils.version_snapshot import build_snapshot

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

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:
            return

        plans = Plan.objects.filter(doelen__persoon=obj).distinct()

        for plan in plans:
            Version.objects.create(
                plan=plan,
                actor=request.user,
                comment="Persoon updated via admin",
                snapshot=build_snapshot(plan),
            )
