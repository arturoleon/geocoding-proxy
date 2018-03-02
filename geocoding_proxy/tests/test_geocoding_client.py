from geocoding_proxy.geocoding_client import GeocodingClient
from rest_framework.test import APITestCase
from mock import Mock
from geocoding_proxy.custom_exceptions import AddressNotFoundException


class GeocodingClientTests(APITestCase):
    """
    Tests for the Geocoding client
    """

    def setUp(self):
        self.client = GeocodingClient()
        self.client.primary_client = Mock()
        self.client.secondary_client = Mock()

    def test_geocoding_fallback(self):
        self.client.primary_client.geocoding = Mock(side_effect=Exception)

        self.client.geocoding("365 N Halsted St, Chicago, IL")

        self.client.secondary_client.geocoding.assert_called_once()

    def test_geocoding_not_founds(self):
        self.client.primary_client.geocoding = Mock(side_effect=Exception)
        self.client.secondary_client.geocoding = Mock(side_effect=AddressNotFoundException)

        with self.assertRaises(AddressNotFoundException):
            self.client.geocoding("365 N Halsted St, Chicago, IL")

        self.client.primary_client.geocoding.assert_called_once()
        self.client.secondary_client.geocoding.assert_called_once()