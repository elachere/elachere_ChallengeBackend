# -*- coding: utf-8 -*-
import json

from rest_framework.response import Response

from groover_challenge import settings
from groover_challenge.http.utils import http_error_handler
from spotiauth.auth import SpotifyAuth

from .utils import BaseUrlSession


class SpotifyClient(SpotifyAuth):
    """
    A client to interact with spotify API.

    (ask_authentication would not be there in a real world case scenario)
    """
    API_BASE_URI = settings.SPOTIFY_API_BASE_URI
    NEW_RELEASES_ENDPOINT = 'browse/new-releases'

    def __init__(self):
        self.token = self.get_or_refresh_token()
        self.session = BaseUrlSession(self.API_BASE_URI)
        self.session.headers.update({'Authorization': f'Bearer {self.token}'})

    def ask_authentication(self):
        auth_uri = self.getUser()
        return Response({
            'message': f'Hello there! Looks like it\'s you\'re first time '
            f'here ! Would please authorize me to get content from your'
            f'Spotify account pleeeeease ?',
            'authorization_link': f'{auth_uri}'
        })

    @http_error_handler
    def fetch_new_releases(self):
        return json.loads(self.session.get(self.NEW_RELEASES_ENDPOINT).text)

    @http_error_handler
    def fetch_artist_infos(self, url):
        return json.loads(self.session.get(url).text)
