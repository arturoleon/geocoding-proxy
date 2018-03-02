from httpclient import HttpClient
import helpers


class HereClient:
    def __init__(self):
        self.app_id = "vAimcDfYzdt8ANZbqC99"
        self.app_code = "ayiOoe1wqUHSYmIiLv_K2A"
        self.http_client = HttpClient()

    def geocoding(self, address):
        url = self.get_url_parameters(address)
        print url
        response = self.http_client.https_get_json(url["domain"], url["path"])
        return self.map_response(response)

    def map_response(self, response):
        return {
            "formatted_address": response["Response"]["View"][0]["Result"][0]["Location"]["Address"]["Label"],
            "location": {
                "latitude": response["Response"]["View"][0]["Result"][0]["Location"]["DisplayPosition"]["Latitude"],
                "longitude": response["Response"]["View"][0]["Result"][0]["Location"]["DisplayPosition"]["Longitude"]
            }
        }

    def get_url_parameters(self, address):
        escaped_address = helpers.format_address(address)
        return {
            "domain": "geocoder.cit.api.here.com",
            "path": "/6.2/geocode.json?app_id={}&app_code={}&searchtext={}"
                .format(self.app_id, self.app_code, escaped_address)
        }