from django.db.models import Prefetch

from openplan.plannen.api.serializers.doel import VersionDoelSerializer
from openplan.plannen.api.serializers.instrument import NestedInstrumentSerializer
from openplan.plannen.api.serializers.persoon import VersionPersoonSerializer
from openplan.plannen.api.serializers.plan import PlanSerializer
from openplan.plannen.models.instrument import Instrument
from openplan.plannen.models.persoon import Persoon
from openplan.plannen.models.relatie import Relatie


def build_snapshot(plan):
    doelen = (
        plan.doelen.select_related("persoon", "doeltype")
        .prefetch_related("instrumenten")
        .all()
    )

    instrumenten = Instrument.objects.filter(doel__plan=plan).distinct()

    personen = (
        Persoon.objects.filter(doelen__plan=plan)
        .distinct()
        .prefetch_related(
            Prefetch(
                "relaties_vanuit",
                queryset=Relatie.objects.select_related(
                    "relatietype", "gerelateerde_persoon"
                ),
            )
        )
    )

    snapshot = {
        "plan": PlanSerializer(plan).data,
        "doelen": VersionDoelSerializer(doelen, many=True).data,
        "instrumenten": NestedInstrumentSerializer(instrumenten, many=True).data,
        "personen": VersionPersoonSerializer(personen, many=True).data,
    }

    return snapshot
