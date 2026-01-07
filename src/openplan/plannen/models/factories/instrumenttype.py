import uuid

import factory

from openplan.plannen.enums.type import InstrumentTypeEnum

from ..instrumenttype import InstrumentType


class InstrumenttypeFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    type = factory.Iterator([choice[0] for choice in InstrumentTypeEnum.choices])

    class Meta:
        model = InstrumentType
