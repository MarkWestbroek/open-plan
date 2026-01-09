import json

from django.contrib import admin
from django.utils.html import format_html

from openplan.plannen.models.version import Version


class VersionAdminInline(admin.StackedInline):
    model = Version
    extra = 0
    max_num = 1
    min_num = 1

    readonly_fields = (
        "plan",
        "version",
        "actor",
        "comment",
        "created_at",
        "snapshot_readonly",
    )
    fields = readonly_fields

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        """
        Only return the last version of the object.
        """
        queryset = super().get_queryset(request)
        parent_id = request.resolver_match.kwargs.get("object_id")
        if not parent_id:
            return queryset.none()

        # Filter for this parent and order by version descending
        last_version = queryset.filter(plan_id=parent_id).order_by("-version").first()
        if not last_version:
            return queryset.none()
        return queryset.filter(id=last_version.id)

    def snapshot_readonly(self, obj):
        if not obj.snapshot:
            return "-"

        plan = obj.snapshot.get("plan")
        doelen = obj.snapshot.get("doelen")
        instrumenten = obj.snapshot.get("instrumenten")
        personen = obj.snapshot.get("personen", [])

        order_personen = [
            {
                "uuid": p.get("uuid"),
                "persoonsprofiel_url": p.get("persoonsprofiel_url"),
                "open_klant_url": p.get("open_klant_url"),
                "bsn": p.get("bsn"),
                "relaties_vanuit": p.get("relaties_vanuit"),
            }
            for p in personen
        ]

        ordered = {
            "plan": plan,
            "doelen": doelen,
            "instrumenten": instrumenten,
            "personen": order_personen,
        }

        return format_html(
            "<pre><code>{}</code></pre>",
            json.dumps(ordered, indent=2),
        )
