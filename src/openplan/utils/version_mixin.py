from django.db import transaction

from openplan.plannen.models.version import Version

from .version_snapshot import build_snapshot


def with_plan_version(*, plan, user, comment, fn):
    with transaction.atomic():
        version = Version.objects.create(
            plan=plan,
            actor=user,
            comment=comment,
        )

        result = fn()

        version.snapshot = build_snapshot(plan)
        version.save(update_fields=["snapshot"])

        return result
