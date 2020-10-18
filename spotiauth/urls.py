# -*- coding: utf-8 -*-
from django.urls import path

from .views import CallbackView, ErrorView, SuccessView

urlpatterns = [
    path('callback/', CallbackView.as_view()),
    path('error/', ErrorView.as_view(), name='error-view'),
    path('success/', SuccessView.as_view(), name='success-view'),
]
