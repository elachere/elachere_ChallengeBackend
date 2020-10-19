# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response

from .client import SpotifyClient
from .models import Artist
from .serializers import ArtistSerializer
from .tasks import sync_new_releases


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
                serializer = ArtistSerializer(artists, many=True)
                return Response({
                    'artists': serializer.data
                })
            sync_new_releases()
            artists = Artist.objects.all()
            serializer = ArtistSerializer(artists, many=True)
            return Response({
                'artists': serializer.data
            })
