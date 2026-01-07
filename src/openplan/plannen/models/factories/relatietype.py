import uuid

import factory

from ..relatietype import RelatieType


class RelatieTypeFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    naam = factory.Sequence(lambda n: f"Relatietype {n}")

    class Meta:
        model = RelatieType
