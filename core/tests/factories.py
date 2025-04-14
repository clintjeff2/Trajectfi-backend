import random

import factory

from core import models


class AcceptedNFTFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AcceptedNFT

    name = factory.Faker("word")

    @factory.lazy_attribute
    def contract_address(self):
        return "0x" + "".join(random.choices("0123456789abcdef", k=60))


class AcceptedTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AcceptedToken

    name = factory.Faker("word")

    @factory.lazy_attribute
    def contract_address(self):
        return "0x" + "".join(random.choices("0123456789abcdef", k=60))
