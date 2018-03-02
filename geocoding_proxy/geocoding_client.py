from google_client import GoogleClient
from here_client import HereClient
from custom_exceptions import AddressNotFoundException
from http_client import HttpClientException

class GeocodingClient():
    def __init__(self):
        self.primary_client = GoogleClient()
        self.secondary_client = HereClient()

    def geocoding(self, address):
        try:
            return self.primary_client.geocoding(address)
        except Exception:
            pass

        try:
            return self.secondary_client.geocoding(address)
        except AddressNotFoundException:
            raise AddressNotFoundException("Address not found.")
