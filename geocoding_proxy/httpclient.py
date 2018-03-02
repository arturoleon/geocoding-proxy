import httplib
import json

class HttpClient:
    def __init__(self):
        self.timeout = 2
        self.httplib = httplib

    def https_get_json(self, domain, path):
        connection = self.httplib.HTTPSConnection(domain, timeout=self.timeout)
        connection.request("GET", path)
        response = connection.getresponse()

        if response.status != 200:
            raise HttpClientException(response.reason)

        return json.loads(response.read())


class HttpClientException(Exception):
    pass
