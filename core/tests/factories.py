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

    token_decimal = factory.Faker("pyint", min_value=6, max_value=18)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    public_key = factory.LazyFunction(
        lambda: "0x" + "".join(random.choices("0123456789abcdef", k=60))
    )


class ListingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Listing

    user = factory.SubFactory("core.factories.UserFactory")
    nft_contract_address = factory.LazyFunction(
        lambda: "0x" + "".join(random.choices("0123456789abcdef", k=60))
    )
    nft_token_id = factory.Sequence(lambda n: n)
    borrow_amount = factory.Faker("pyint", min_value=100, max_value=10000)
    repayment_amount = factory.Faker("pyint", min_value=110, max_value=11000)
    duration = factory.Faker("pyint", min_value=1, max_value=365)
    status = models.ListingStatus.OPEN
