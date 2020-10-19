# -*- coding: utf-8 -*-
from django.urls import path

from .views import AuthorizationView, CallbackView, ErrorView, SuccessView

app_name = 'spotiauth'

urlpatterns = [
    path('authorization/', AuthorizationView.as_view(), name='authorization'),
    path('callback/', CallbackView.as_view(), name='callback'),
    path('error/', ErrorView.as_view(), name='error-view'),
    path('success/', SuccessView.as_view(), name='success-view'),
]
