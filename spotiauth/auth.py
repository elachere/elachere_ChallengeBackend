# -*- coding: utf-8
import json
import requests
import base64

from datetime import timedelta

from django.utils import timezone
from django.utils.http import urlencode

from groover_challenge import settings

from .models import SpotifyToken


class SpotifyAuth:
    CLIENT_ID = settings.SPOTIFY_CLIENT_ID
    CLIENT_SECRET = settings.SPOTIFY_CLIENT_SECRET
    CALLBACK_URL = settings.SPOTIFY_CALLBACK_URI
    AUTHORIZATION_URI = settings.SPOTIFY_AUTH_URI
    TOKEN_URI = settings.SPOTIFY_TOKEN_URI
    BASE_URI = settings.SPOTIFY_API_BASE_URI
    RESPONSE_TYPE = "code"
    HEADER = "application/x-www-form-urlencoded"
    SCOPE = "user-read-email user-read-private"

    def get_or_refresh_token(self):
        token = SpotifyToken.objects.last()
        if token is None:
            return None
        elif token.expiration < timezone.now():
            token_response = self.refreshAuth(token.refresh)
            token.access = token_response['access_token']
            token.expiration = timezone.now() + timedelta(seconds=token_response['expires_in'])
            token.save()

        return token.access

    def getUserEmail(self, token):
        post = requests.get(f'{self.BASE_URI}me', headers={'Authorization': f'Bearer {token}'})
        return json.loads(post.text)['email']

    def getAuth(self, client_id, redirect_uri, scope):
        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'scope': scope,
            'response_type': 'code'
        }
        encoded = urlencode(params)
        return f'{self.AUTHORIZATION_URI}?{encoded}'

    def getToken(self, code, client_id, client_secret, redirect_uri):
        body = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        headers = {
            "Content-Type": self.HEADER,
        }

        post = requests.post(self.TOKEN_URI, params=body, headers=headers)
        return self.handleToken(json.loads(post.text))

    def handleToken(self, response, refresh=False):
        keys = ["access_token", "expires_in"]

        if "error" in response:
            return response
        if not refresh:
            keys.append("refresh_token")
        return {
            key: response[key] for key in keys
        }

    def refreshAuth(self, refresh_token):
        encoded = base64.b64encode(f"{self.CLIENT_ID}:{self.CLIENT_SECRET}".encode()).decode()
        headers = {
            "Content-Type": self.HEADER,
            "Authorization": f"Basic {encoded}",
        }
        body = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }

        post_refresh = requests.post(
            self.TOKEN_URI, data=body, headers=headers
        )

        return self.handleToken(json.loads(post_refresh.text), refresh=True)

    def getUser(self):
        return self.getAuth(
            self.CLIENT_ID, f"{self.CALLBACK_URL}/callback", self.SCOPE,
        )

    def getUserToken(self, code):
        return self.getToken(
            code, self.CLIENT_ID, self.CLIENT_SECRET, f"{self.CALLBACK_URL}/callback"
        )
