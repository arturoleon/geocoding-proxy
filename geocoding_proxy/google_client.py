import httplib
import urllib
from httpclient import HttpClient

"""
TODO:
- URL encode address
- Move format_address to helper
- Throw exception if mapping fails
"""


class GoogleClient:
    def __init__(self):
        self.api_key = "AIzaSyAKcHpDwduyAGfLkfqwnYr9nwSPq1AYvp4"

    def geocoding(self, address):
        url = self.get_url_parameters(address)
        client = HttpClient()
        response = client.https_get_json(url["domain"], url["path"])
        print self.map_response(response)

    def map_response(self, response):
        return {
            "formatted_address": response["results"][0]["formatted_address"],
            "location": {
                "latitude": response["results"][0]["geometry"]["location"]["lat"],
                "longitude": response["results"][0]["geometry"]["location"]["lng"]
            }
        }

    def get_url_parameters(self, address):
        escaped_address = self.format_address(address)
        return {
            "domain": "maps.googleapis.com",
            "path": "/maps/api/geocode/json?address={}&key={}".format(escaped_address, self.api_key)
        }

    @staticmethod
    def format_address(address):
        return urllib.quote(address)