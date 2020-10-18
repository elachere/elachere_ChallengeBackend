# -*- coding: utf-8 -*-
from datetime import timedelta

from django.utils import timezone
from django.shortcuts import redirect
from django.views.generic import TemplateView

from rest_framework.views import APIView
from rest_framework.response import Response

from .auth import SpotifyAuth
from .models import SpotifyToken


class ErrorView(TemplateView):
    pass


class SuccessView(TemplateView):
    pass


class CallbackView(APIView):
    """
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
            print(token_response)
            return redirect('error-view')

        token = SpotifyToken(
            access=token_response['access_token'],
            refresh=token_response['refresh_token'],
            expiration=timezone.now() + timedelta(seconds=token_response['expires_in'])
        )
        token.save()

        return redirect('success-view')
