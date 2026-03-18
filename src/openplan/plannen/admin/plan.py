from django.contrib import admin

from ..models.plan import Plan, PlanState


class PlanStateInline(admin.TabularInline):
    model = PlanState
    extra = 0
    readonly_fields = ("recorded_at", "changed_by", "startdatum", "einddatum")
    fields = (
        "startdatum",
        "einddatum",
        "titel",
        "status",
        "fase",
        "notitie",
        "reden_einde",
        "changed_by",
        "recorded_at",
    )
    show_change_link = True


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "current_titel",
        "overkoepelend_plan",
        "plantype",
        "current_status",
        "current_fase",
        "startdatum",
    )

    list_filter = (
        "plantype",
        "states__status",
    )

    search_fields = ("uuid", "current_titel")

    readonly_fields = ("uuid",)

    inlines = (PlanStateInline,)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uuid",
                    "plantype",
                    "overkoepelend_plan",
                    "zaak",
                    "domeinregister",
                    "medewerker",
                ),
            },
        ),
        (
            "Huidige State",
            {
                "fields": (
                    "current_titel",
                    "current_status",
                    "current_fase",
                    "current_notitie",
                    "current_reden_einde",
                    "startdatum",
                    "einddatum",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        # prefetch related states for efficiency
        qs = super().get_queryset(request)
        return qs.prefetch_related("states")

    # helpers to show current state fields
    def current_titel(self, obj):
        return obj.current_state.titel if obj.current_state else ""

    current_titel.short_description = "Titel"

    def current_status(self, obj):
        return obj.current_state.status if obj.current_state else ""

    current_status.short_description = "Status"

    def current_fase(self, obj):
        return obj.current_state.fase if obj.current_state else ""

    current_fase.short_description = "Fase"

    def current_notitie(self, obj):
        return obj.current_state.notitie if obj.current_state else ""

    current_notitie.short_description = "Notitie"

    def current_reden_einde(self, obj):
        return obj.current_state.reden_einde if obj.current_state else ""

    current_reden_einde.short_description = "Reden Einde"
