# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response

from .client import SpotifyClient
from .models import Artist
from .serializers import ArtistSerializer


class ArtistView(APIView):
    """
    """

    def get(self, request):
        client = SpotifyClient()
        if client.token is None:
            return client.ask_authentication()
        else:
            artists = Artist.objects.all()
            if len(artists):
                # serialize and return
            # launch celery task
               pass
