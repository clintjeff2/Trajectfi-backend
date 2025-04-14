from django.urls import reverse
from rest_framework.test import APITestCase

from . import factories


class TestAcceptedTokenListAPIView(APITestCase):
    def setUp(self):
        self.url = reverse("accepted-tokens-list-view")

    def test_accepted_token_list_view_successful(self):
        """
        Test for the success response of the api
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_accepted_token_list_view_with_data(self):
        """
        Test for the success response of the api with data in the db
        """
        self._generate_data()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 3)

    def _generate_data(self):
        """
        Generate mock data in the db using the factory
        """
        factories.AcceptedTokenFactory()
        factories.AcceptedTokenFactory()
        factories.AcceptedTokenFactory()
