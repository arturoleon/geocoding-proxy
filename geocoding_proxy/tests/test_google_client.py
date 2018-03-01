from geocoding_proxy.google_client import GoogleClient
from rest_framework.test import APITestCase
from mock import Mock


class GoogleClientTests(APITestCase):
    """
    Tests for the GoogleClient for Geocoding API
    """

    def test_get_url_parameters(self):
        client = GoogleClient()
        client.api_key = "abc123"
        response = client.get_url_parameters("Google Building 41, 1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA")

        self.assertEqual(response["domain"], "maps.googleapis.com")
        self.assertEqual(response["path"], "/maps/api/geocode/json?address=Google%20Building%2041%2C%201600"
                                           "%20Amphitheatre%20Pkwy%2C%20Mountain%20View%2C%20CA%2094043%2C%20USA&key"
                                           "=abc123")

    def test_map_response(self):
        client = GoogleClient()
        input_object = {
            "results": [
                {
                    "formatted_address": "Google Building 41, 1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA",
                    "geometry": {
                        "location": {
                            "lat": 37.4221145,
                            "lng": -122.0860002
                        }
                    }
                }
            ]
        }

        response = client.map_response(input_object)

        self.assertEqual(response["formatted_address"],
                         "Google Building 41, 1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA")
        self.assertEqual(response["location"]["latitude"], 37.4221145)
        self.assertEqual(response["location"]["longitude"], -122.0860002)
