# -*- coding: utf-8 -*-
from django.urls import path

from .views import ArtistView

app_name = 'spotifetcher'

urlpatterns = [
    path('artists/', ArtistView.as_view(), name='artists-list'),
]
