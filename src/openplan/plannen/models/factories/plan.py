import uuid

import factory

from ..plan import Plan
from .plantype import PlanTypeFactory


class PlanFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    plantype = factory.SubFactory(PlanTypeFactory)

    class Meta:
        model = Plan
