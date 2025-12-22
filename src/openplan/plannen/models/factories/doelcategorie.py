import uuid

import factory

from ..doelcategorie import DoelCategorie


class DoelCategorieFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    naam = factory.Sequence(lambda n: f"Doel {n}")

    class Meta:
        model = DoelCategorie
