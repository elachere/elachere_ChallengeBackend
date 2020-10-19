# -*- coding: utf-8 -*-

from django.db.models import (
    Model, CharField, IntegerField, ManyToManyField, URLField
)


class Genre(Model):
    """
    """
    name = CharField(max_length=32)

    @classmethod
    def classname(cls):
        return 'Genre'


class Image(Model):
    """
    """
    height = IntegerField()
    width = IntegerField()
    url = URLField()

    @classmethod
    def classname(cls):
        return 'Image'


class Artist(Model):
    """
    """
    id = CharField(max_length=32, unique=True, primary_key=True)
    name = CharField(max_length=32, unique=True)
    popularity = IntegerField()
    followers = IntegerField()

    genres = ManyToManyField(Genre)
    images = ManyToManyField(Image)
