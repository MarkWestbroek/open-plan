import uuid

import factory

from openplan.plannen.enums.status import PlanStatus

from ..overkoepelendplan import OverkoepelendPlan


class OverkoepelendPlanFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    titel = factory.Faker("sentence", nb_words=4)
    status = PlanStatus.ACTIEF

    class Meta:
        model = OverkoepelendPlan
