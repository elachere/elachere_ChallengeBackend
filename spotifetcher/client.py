# -*- coding: utf-8 -*-
from spotiauth.auth import SpotifyAuth
from rest_framework.response import Response


class SpotifyClient(SpotifyAuth):
    """
    """
    def __init__(self):
        self.token = self.get_or_refresh_token()

    def ask_authentication(self):
        auth_uri = SpotifyAuth().getUser()
        return Response({
            'message': f'Hello there! Looks like it\'s you\'re first time'
            f'here ! Would please authorize me to get content from your'
            f'Spotify account pleeeeease ?',
            'authorization_link': f'{auth_uri}'
        })
