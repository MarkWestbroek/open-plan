import uuid

import factory

from openplan.plannen.models.contactmoment import Contactmoment

from .plan import PlanFactory


class ContactmomentFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    plan = factory.SubFactory(PlanFactory)

    class Meta:
        model = Contactmoment
