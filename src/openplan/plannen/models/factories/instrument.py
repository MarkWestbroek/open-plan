import uuid

import factory

from ..instrument import Instrument
from .doel import DoelFactory
from .instrumenttype import InstrumenttypeFactory


class InstrumentFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    doel = factory.SubFactory(DoelFactory)
    instrumenttype = factory.SubFactory(InstrumenttypeFactory)

    class Meta:
        model = Instrument
