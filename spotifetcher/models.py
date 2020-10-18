# -*- coding: utf-8 -*-

from django.db.models import (
    Model, CharField, IntegerField, ManyToManyField, URLField
)


class Genre(Model):
    """
    """
    name = CharField(max_length=16)


class Image(Model):
    """
    """
    height = IntegerField()
    width = IntegerField()
    url = URLField()


class Artist(Model):
    """
    """
    id = CharField(max_length=32, unique=True, primary_key=True)
    name = CharField(max_length=32, unique=True)
    popularity = IntegerField()
    followers = IntegerField()

    genres = ManyToManyField(Genre)
    images = ManyToManyField(Image)
