import uuid

import factory

from openplan.plannen.enums.type import InstrumentTypeEnum
from openplan.plannen.models.factories.instrumentcategorie import (
    InstrumentCategorieFactory,
)

from ..instrumenttype import InstrumentType


class InstrumenttypeFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    instrument_type = factory.Iterator(
        [choice[0] for choice in InstrumentTypeEnum.choices]
    )

    class Meta:
        model = InstrumentType

    @factory.post_generation
    def categorieen(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for cat in extracted:
                self.categorieen.add(cat)
        else:
            self.categorieen.add(InstrumentCategorieFactory.create())
