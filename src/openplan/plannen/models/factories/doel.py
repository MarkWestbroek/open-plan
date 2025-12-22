import uuid

import factory

from ..doel import Doel
from .doeltype import DoelTypeFactory
from .persoon import PersoonFactory
from .plan import PlanFactory


class DoelFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    doeltype = factory.SubFactory(DoelTypeFactory)
    plan = factory.SubFactory(PlanFactory)
    persoon = factory.SubFactory(PersoonFactory)
    hoofd_doel = None

    class Meta:
        model = Doel
