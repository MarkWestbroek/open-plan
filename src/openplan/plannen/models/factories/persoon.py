import uuid

import factory

from ..persoon import Persoon


class PersoonFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)

    class Meta:
        model = Persoon
