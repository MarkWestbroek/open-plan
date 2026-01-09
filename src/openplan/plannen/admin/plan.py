from django.contrib import admin

from openplan.plannen.models.version import Version
from openplan.utils.version_snapshot import build_snapshot

from ..models.plan import Plan
from .version import VersionAdminInline


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    inlines = [VersionAdminInline]
    list_display = (
        "uuid",
        "plantype",
    )
    list_filter = ("plantype",)
    # search_fields = ("uuid", "plantype__naam")
    ordering = ("-pk",)
    readonly_fields = ("uuid",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uuid",
                    "plantype",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("plantype")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:
            return

        Version.objects.create(
            plan=obj,
            actor=request.user,
            comment="Plan updated via admin",
            snapshot=build_snapshot(obj),
        )
