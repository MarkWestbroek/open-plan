import uuid

from django.utils import timezone

import factory

from openplan.plannen.enums.status import PlanStatus
from openplan.plannen.models.factories.doel import DoelFactory

from ..instrument import Instrument
from .instrumentcategorie import InstrumentCategorieFactory
from .instrumenttype import InstrumenttypeFactory


class InstrumentFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    instrumenttype = factory.SubFactory(InstrumenttypeFactory)
    titel = factory.Faker("sentence", nb_words=3)
    startdatum = factory.LazyFunction(timezone.now)

    status = PlanStatus.ACTIEF

    class Meta:
        model = Instrument

    @factory.post_generation
    def doelen(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for doel in extracted:
                self.doelen.add(doel)
        else:
            self.doelen.add(DoelFactory.create())

    @factory.post_generation
    def instrument_categorieen(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for categorie in extracted:
                self.instrument_categorieen.add(categorie)
        else:
            self.instrument_categorieen.add(InstrumentCategorieFactory.create())

    @factory.post_generation
    def ontwikkelwensen(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for ow in extracted:
                self.ontwikkelwensen.add(ow)
