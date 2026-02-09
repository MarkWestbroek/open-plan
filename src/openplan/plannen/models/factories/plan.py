import uuid

from django.utils import timezone

import factory

from openplan.plannen.enums.status import PlanStatus

from ..plan import Plan
from .overkoepelendplan import OverkoepelendPlanFactory
from .plantype import PlanTypeFactory


class PlanFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)

    overkoepelend_plan = factory.SubFactory(OverkoepelendPlanFactory)
    plantype = factory.SubFactory(PlanTypeFactory)

    titel = factory.Faker("sentence", nb_words=4)
    status = PlanStatus.ACTIEF
    startdatum = factory.LazyFunction(timezone.now)

    class Meta:
        model = Plan
