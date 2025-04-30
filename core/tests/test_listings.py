import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from core.models import ListingStatus
from core.tests import factories


@pytest.mark.django_db
def test_list_active_listings():
    client = APIClient()
    url = reverse("listing-list")

    user = factories.UserFactory()

    active_listing = factories.ListingFactory(user=user, status=ListingStatus.OPEN)
    factories.ListingFactory(user=user, status=ListingStatus.CLOSED)

    response = client.get(url)
    assert response.status_code == 200

    data = response.json()
    results = data["results"]
    assert len(results) == 1

    listing = results[0]
    assert listing["listing_id"] == str(active_listing.id)
    assert listing["collateral_contract"] == active_listing.nft_contract_address
    assert listing["collateral_id"] == active_listing.nft_token_id
    assert listing["borrower_address"] == active_listing.user.public_key
    assert listing["loan_amount"] == active_listing.borrow_amount
    assert listing["loan_duration"] == active_listing.duration
    assert listing["status"] == active_listing.status


@pytest.mark.django_db
def test_listings_filter_by_collateral_contract():
    client = APIClient()
    url = reverse("listing-list")

    user = factories.UserFactory()
    factories.ListingFactory(
        user=user, nft_contract_address="0xFilterThis", status=ListingStatus.OPEN
    )

    response = client.get(url, {"collateral_contract": "0xFilterThis"})
    assert response.status_code == 200

    data = response.json()
    results = data["results"]
    assert len(results) == 1
    assert results[0]["collateral_contract"] == "0xFilterThis"


@pytest.mark.django_db
def test_listings_filter_by_borrower_address():
    client = APIClient()
    url = reverse("listing-list")

    user = factories.UserFactory(public_key="0xBorrowerFilter")
    factories.ListingFactory(user=user, status=ListingStatus.OPEN)

    response = client.get(url, {"borrower_address": "0xBorrowerFilter"})
    assert response.status_code == 200

    data = response.json()
    results = data["results"]
    assert len(results) == 1
    assert results[0]["borrower_address"] == "0xBorrowerFilter"
