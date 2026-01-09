from django.db import models
from django.utils.translation import gettext_lazy as _

from openplan.plannen.models.plan import Plan
from openplan.utils.version_snapshot import build_snapshot


class Version(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="versies")
    version = models.PositiveSmallIntegerField(
        _("version"), help_text=_("Versie van het Plan.")
    )
    actor = models.ForeignKey("accounts.User", null=True, on_delete=models.SET_NULL)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    snapshot = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = _("Version")
        verbose_name_plural = _("Versions")

    def __str__(self):
        return f"{self.plan} - {self.actor} - {self.created_at}"

    def save(self, *args, **kwargs):
        if not self.version:
            self.version = self.generate_version_number()

        if self.snapshot is None:
            self.snapshot = build_snapshot(self.plan)

        super().save(*args, **kwargs)

    def generate_version_number(self) -> int:
        existed_versions = Version.objects.filter(plan=self.plan)

        max_version = 0
        if existed_versions.exists():
            max_version = existed_versions.aggregate(models.Max("version"))[
                "version__max"
            ]

        version_number = max_version + 1
        return version_number
