import os
from http_client import HttpClient
import helpers
from custom_exceptions import AddressNotFoundException


class GoogleClient:
    """
    Implements the Google Geocoding API service. 
    """
    def __init__(self):
        self.api_key = os.environ.get('GOOGLE_API_KEY')
        self.http_client = HttpClient()

    def geocoding(self, address):
        url = self.get_url_parameters(address)
        response = self.http_client.https_get_json(url["domain"], url["path"])
        return self.map_response(response)

    def map_response(self, response):
        """
        Assumes that the first response is the _best_ match. If it fails to map means that we got an empty or unexpected
        response.
        """
        try:
            return {
                "formatted_address": response["results"][0]["formatted_address"],
                "location": {
                    "latitude": response["results"][0]["geometry"]["location"]["lat"],
                    "longitude": response["results"][0]["geometry"]["location"]["lng"]
                }
            }
        except AddressNotFoundException:
            raise AddressNotFoundException()

    def get_url_parameters(self, address):
        """
        Generates the URL we need to query the service. Is broken up into two parts as the http_client module requires.
        """
        escaped_address = helpers.format_address(address)
        return {
            "domain": "maps.googleapis.com",
            "path": "/maps/api/geocode/json?address={}&key={}".format(escaped_address, self.api_key)
        }

