# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response

from .client import SpotifyClient
from .models import Artist
from .serializers import ArtistSerializer
from .tasks import sync_new_releases


class ArtistView(APIView):
    """
    View to return data about artists.

    For the purpose of this challenge we handle authentication if we don't have
    a token yet, but in a real world case scenario users would have to
    authenticate first before accessing this view.

    Fetch artists and return serialized data if db is populated, else launch
    a synchronization.
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
