# -*- coding: utf-8 -*-
from django.urls import path

from .views import ArtistView

urlpatterns = [
    path('artists/', ArtistView.as_view()),
]
