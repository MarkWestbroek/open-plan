from django.contrib import admin

from ..models.doeltype import DoelType


@admin.register(DoelType)
class DoelTypeAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "doel_type",
    )
    list_filter = ("doel_type",)
    search_fields = ("doel_type", "uuid")
    ordering = ("doel_type",)
    readonly_fields = ("uuid",)
    filter_horizontal = ("categorieen",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uuid",
                    "doel_type",
                    "categorieen",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("categorieen")
