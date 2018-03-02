from http_client import HttpClient
import helpers
from custom_exceptions import AddressNotFoundException


class GoogleClient:
    def __init__(self):
        self.api_key = "AIzaSyAKcHpDwduyAGfLkfqwnYr9nwSPq1AYvp4"
        self.http_client = HttpClient()

    def geocoding(self, address):
        url = self.get_url_parameters(address)
        response = self.http_client.https_get_json(url["domain"], url["path"])
        return self.map_response(response)

    def map_response(self, response):
        try:
            return {
                "formatted_address": response["results"][0]["formatted_address"],
                "location": {
                    "latitude": response["results"][0]["geometry"]["location"]["lat"],
                    "longitude": response["results"][0]["geometry"]["location"]["lng"]
                }
            }
        except AddressNotFoundException:
            raise AddressNotFoundException("Not found")

    def get_url_parameters(self, address):
        escaped_address = helpers.format_address(address)
        return {
            "domain": "maps.googleapis.com",
            "path": "/maps/api/geocode/json?address={}&key={}".format(escaped_address, self.api_key)
        }

