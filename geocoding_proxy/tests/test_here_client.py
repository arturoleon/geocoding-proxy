from geocoding_proxy.here_client import HereClient
from rest_framework.test import APITestCase
from mock import Mock


class HereClientTests(APITestCase):
    """
    Tests for the HereClient for Geocoding API
    """

    def setUp(self):
        self.client = HereClient()
        self.client.app_code = "abc123"
        self.client.app_id = "id987"

    def test_get_url_parameters(self):
        response = self.client.get_url_parameters(
            "365 N Halsted St Chicago, 60661")

        self.assertEqual(response["domain"], "geocoder.cit.api.here.com")
        self.assertEqual(response["path"], "/6.2/geocode.json?app_id=id987&app_code=abc123&searchtext=365%20N"
                                           "%20Halsted%20St%20Chicago%2C%2060661")

    def test_map_response(self):
        input_object = {
            "Response": {
                "View": [
                    {
                        "Result": [
                            {
                                "Location": {
                                    "Address": {
                                        "Label": "365 N Halsted St, Chicago, IL 60661, United States"
                                    },
                                    "DisplayPosition": {
                                            "Latitude": 37.4221145,
                                            "Longitude": -122.0860002
                                    }
                                }
                            }
                        ]
                    }
                ]
            }
        }

        response = self.client.map_response(input_object)

        self.assertEqual(response["formatted_address"], "365 N Halsted St, Chicago, IL 60661, United States")
        self.assertEqual(response["location"]["latitude"], 37.4221145)
        self.assertEqual(response["location"]["longitude"], -122.0860002)

    def test_geocoding(self):
        response_object = {
            "Response": {
                "View": [
                    {
                        "Result": [
                            {
                                "Location": {
                                    "Address": {
                                        "Label": "365 N Halsted St, Chicago, IL 60661, United States"
                                    },
                                    "DisplayPosition": {
                                            "Latitude": 37.4221145,
                                            "Longitude": -122.0860002
                                    }
                                }
                            }
                        ]
                    }
                ]
            }
        }

        self.client.http_client = Mock()
        self.client.http_client.https_get_json.return_value = response_object
        self.client.http_client.get_url_parameters.return_value = {"domain": "arturoleon.net", "path": "/"}

        response = self.client.geocoding("365 N Halsted St, Chicago, IL")

        self.assertEqual(response["formatted_address"], "365 N Halsted St, Chicago, IL 60661, United States")
        self.assertEqual(response["location"]["latitude"], 37.4221145)
        self.assertEqual(response["location"]["longitude"], -122.0860002)
