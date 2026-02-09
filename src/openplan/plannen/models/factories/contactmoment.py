import uuid

from django.utils import timezone

import factory

from openplan.plannen.models.contactmoment import Contactmoment

from .plan import PlanFactory


class ContactmomentFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    plan = factory.SubFactory(PlanFactory)
    datum = factory.LazyFunction(timezone.now)

    class Meta:
        model = Contactmoment
