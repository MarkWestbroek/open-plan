import uuid

import factory

from openplan.plannen.enums.type import PlanTypeEnum

from ..plantype import PlanType


class PlanTypeFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    type = factory.Iterator([choice[0] for choice in PlanTypeEnum.choices])

    class Meta:
        model = PlanType
