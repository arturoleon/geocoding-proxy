# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from django.http import JsonResponse
from google_client import GoogleClient

from django.shortcuts import render


class Geocoding(APIView):
    def get(self, request):
        """
        GET /geocoding?address={}
        """
        response = GoogleClient().geocoding(request.query_params["address"])
        return JsonResponse(response)
