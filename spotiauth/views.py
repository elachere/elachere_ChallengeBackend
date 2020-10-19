# -*- coding: utf-8 -*-
from datetime import timedelta

from django.utils import timezone
from django.shortcuts import redirect
from django.views.generic import TemplateView

from rest_framework.views import APIView
from rest_framework.response import Response

from .auth import SpotifyAuth
from .models import SpotifyToken, SpotifyUser


class ErrorView(TemplateView):
    """
    View to show in case of auth failure.
    """
    pass


class SuccessView(TemplateView):
    """
    View to show in case of auth success.
    """
    pass


class AuthorizationView(APIView):
    """
    View to generate an authentication link to give to the user.
    """

    def get(self, request):
        auth_uri = SpotifyAuth().getUser()
        return Response({
            'message': f'Hello there! Looks like it\'s you\'re first time'
            f'here ! Would please authorize me to get content from your'
            f'Spotify account pleeeeease ?',
            'authorization_link': f'{auth_uri}'
        })


class CallbackView(APIView):
    """
    View to handle oAuth2 callback.

    Save the received token, and associate it to a newly created `user` (here
    the user model is pretty useless since the app does not handle multiple
    user).
    """

    def get(self, request):
        code = request.GET.get('code')
        if code is None:
            error = request.GET.get('error', 'Unknown error')
            return Response({
                'error': f'{error}'
            })

        auth_client = SpotifyAuth()
        token_response = auth_client.getUserToken(code)

        if 'error' in token_response:
            return redirect('error-view')

        token = SpotifyToken(
            access=token_response['access_token'],
            refresh=token_response['refresh_token'],
            expiration=timezone.now() + timedelta(seconds=token_response['expires_in'])
        )
        token.save()

        email = auth_client.getUserEmail(token.access)
        user = SpotifyUser(email=email, token=token)
        user.save()

        return redirect('success-view')
