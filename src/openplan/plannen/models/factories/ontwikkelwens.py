import uuid

from django.utils import timezone

import factory

from openplan.plannen.enums.status import PlanStatus
from openplan.plannen.models.factories.doel import DoelFactory
from openplan.plannen.models.factories.doelcategorie import DoelCategorieFactory
from openplan.plannen.models.ontwikkelwens import Ontwikkelwens


class OntwikkelwensFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    doel = factory.SubFactory(DoelFactory)
    status = PlanStatus.ACTIEF
    titel = factory.Faker("sentence", nb_words=4)
    beschrijving = factory.Faker("paragraph")
    startdatum = factory.LazyFunction(timezone.now)

    class Meta:
        model = Ontwikkelwens

    @factory.post_generation
    def doel_categorieen(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for categorie in extracted:
                self.doel_categorieen.add(categorie)
        else:
            self.doel_categorieen.add(DoelCategorieFactory.create())
