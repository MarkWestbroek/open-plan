import uuid

import factory

from ..relatie import Relatie
from .persoon import PersoonFactory
from .relatietype import RelatieTypeFactory


class RelatieFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)

    persoon = factory.SubFactory(PersoonFactory)
    gerelateerde_persoon = factory.SubFactory(PersoonFactory)
    relatietype = factory.SubFactory(RelatieTypeFactory)

    class Meta:
        model = Relatie
