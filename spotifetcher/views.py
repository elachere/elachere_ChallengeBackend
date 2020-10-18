# -*- coding: utf-8 -*-
from rest_framework.views import APIView

from .client import SpotifyClient


class ArtistView(APIView):
    """
    """

    def get(self, request):
        client = SpotifyClient()
        if client.token is None:
            return client.ask_authentication()
        else:
            pass
