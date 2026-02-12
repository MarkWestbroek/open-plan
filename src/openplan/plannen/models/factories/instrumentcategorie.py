import uuid

import factory

from ..instrumentcategorie import InstrumentCategorie


class InstrumentCategorieFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    naam = factory.Sequence(lambda n: f"Instrument {n}")

    class Meta:
        model = InstrumentCategorie
