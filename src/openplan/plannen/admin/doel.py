from django.contrib import admin

from openplan.plannen.admin.plan import build_snapshot
from openplan.plannen.models.version import Version

from ..models.doel import Doel


@admin.register(Doel)
class DoelAdmin(admin.ModelAdmin):
    list_display = (
        "plan",
        "persoon",
    )
    list_filter = ("plan",)
    # search_fields = ("uuid", "persoon__naam", "plan__naam")
    ordering = ("-pk",)
    readonly_fields = ("uuid",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uuid",
                    "doeltype",
                    "plan",
                    "persoon",
                    "hoofd_doel",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("plan", "persoon")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:
            return

        Version.objects.create(
            plan=obj.plan,
            actor=request.user,
            comment="Doel updated via admin",
            snapshot=build_snapshot(obj.plan),
        )
