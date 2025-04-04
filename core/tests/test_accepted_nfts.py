from django.urls import reverse
from rest_framework.test import APITestCase

from . import factories


class TestAcceptedNFTListAPIView(APITestCase):
    def setUp(self):
        self.url = reverse("accepted-nfts-list-view")

    def test_accepted_nft_list_view_successful(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_accepted_nft_list_view_with_data(self):
        self._generate_data()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 3)

    def _generate_data(self):
        factories.AcceptedNFTFactory()
        factories.AcceptedNFTFactory()
        factories.AcceptedNFTFactory()
