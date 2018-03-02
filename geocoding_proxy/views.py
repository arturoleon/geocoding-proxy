# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from django.http import JsonResponse
from geocoding_client import GeocodingClient
from custom_exceptions import AddressNotFoundException
from http_client import HttpClientException

from django.shortcuts import render


class Geocoding(APIView):
    def get(self, request):
        """
        GET /geocoding?address={}
        """
        try:
            response = GeocodingClient().geocoding(request.query_params["address"])
            return JsonResponse(response)
        except AddressNotFoundException as e:
            error_response = JsonResponse({"error": e.message})
            error_response.status_code = 404
            return error_response
        except HttpClientException as e:
            error_response = JsonResponse({"error": e.message})
            error_response.status_code = e.status_code
            return error_response
