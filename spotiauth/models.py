# -*- coding: utf-8 -*-
from django.db.models import (
    Model, DateTimeField, EmailField, OneToOneField, CASCADE
)

from encrypted_fields import fields

from groover_challenge import settings


HASH_KEY = settings.FIELD_ENCRYPTION_KEYS[0]


class SpotifyToken(Model):
    """
    Describe a spotify token. Self explenatory.
    """
    _access = fields.EncryptedCharField(max_length=256)
    access = fields.SearchField(hash_key=HASH_KEY,
                                encrypted_field_name='_access')
    _refresh = fields.EncryptedCharField(max_length=256)
    refresh = fields.SearchField(hash_key=HASH_KEY,
                                 encrypted_field_name='_refresh')
    expiration = DateTimeField()


class SpotifyUser(Model):
    """
    Describe a spotify user.

    Here this model is pretty useless since we don't handle multiple users with
    registration and authentication to the app, but in a real word case
    scenario we would ask users to authenticate to the app first, and then
    use its associated token.
    """
    email = EmailField(unique=True)

    token = OneToOneField('SpotifyToken', on_delete=CASCADE,
                          related_name='users')
