import uuid

import factory

from openplan.plannen.enums.doel import DoelTypeEnum

from ..doeltype import DoelType


class DoelTypeFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    type = factory.Iterator([choice[0] for choice in DoelTypeEnum.choices])

    class Meta:
        model = DoelType
