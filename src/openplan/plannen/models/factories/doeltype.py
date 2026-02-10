import uuid

import factory

from openplan.plannen.enums.doel import DoelTypeEnum
from openplan.plannen.models.factories.doelcategorie import DoelCategorieFactory

from ..doeltype import DoelType


class DoelTypeFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    doel_type = factory.Iterator([choice[0] for choice in DoelTypeEnum.choices])

    class Meta:
        model = DoelType

    @factory.post_generation
    def categorieen(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for cat in extracted:
                self.categorieen.add(cat)
        else:
            self.categorieen.add(DoelCategorieFactory.create())
