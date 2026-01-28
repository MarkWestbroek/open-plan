import uuid

import factory

from ..persoon import Persoon


class PersoonFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    persoonsprofiel = "urn:persoon:profiel:123"
    klant = "urn:klant:123"
    bsn = "123456789"

    class Meta:
        model = Persoon
