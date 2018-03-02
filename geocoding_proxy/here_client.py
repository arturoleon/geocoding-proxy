import os
from http_client import HttpClient
import helpers
from custom_exceptions import AddressNotFoundException


class HereClient:
    """
    Implements the HERE Geocoding API service. 
    """
    def __init__(self):
        self.app_id = os.environ.get('HERE_APP_ID')
        self.app_code = os.environ.get('HERE_APP_CODE')
        self.http_client = HttpClient()

    def geocoding(self, address):
        url = self.get_url_parameters(address)
        print url
        response = self.http_client.https_get_json(url["domain"], url["path"])
        return self.map_response(response)

    def map_response(self, response):
        """
        Assumes that the first response is the _best_ match. If it fails to map means that we got an empty or unexpected
        response.
        """
        try:
            return {
                "formatted_address": response["Response"]["View"][0]["Result"][0]["Location"]["Address"]["Label"],
                "location": {
                    "latitude": response["Response"]["View"][0]["Result"][0]["Location"]["DisplayPosition"]["Latitude"],
                    "longitude": response["Response"]["View"][0]["Result"][0]["Location"]["DisplayPosition"][
                        "Longitude"]
                }
            }
        except IndexError:
            raise AddressNotFoundException()

    def get_url_parameters(self, address):
        """
        Generates the URL we need to query the service. Is broken up into two parts as the http_client module requires.
        """
        escaped_address = helpers.format_address(address)
        return {
            "domain": "geocoder.cit.api.here.com",
            "path": "/6.2/geocode.json?app_id={}&app_code={}&searchtext={}"
                .format(self.app_id, self.app_code, escaped_address)
        }
