# -*- coding: utf-8 -*-
import logging

from celery import shared_task

from .client import SpotifyClient
from .models import Genre, Image
from .serializers import ArtistSerializer


logger = logging.getLogger(__name__)


class UnauthorizedException(Exception):
    pass


def get_or_create(obj_key, db_objects, model, attrs):
    model_name = model.classname()
    if obj_key in db_objects[model_name]:
        obj = db_objects[model_name][obj_key]
    else:
        try:
            obj = model.objects.get(**attrs)
        except model.DoesNotExist:
            logger.info(f'Creating new {model_name} <{obj_key}>')
            obj = model(**attrs)
            obj.save()
        finally:
            db_objects[model_name][obj_key] = obj

    return obj


def serialize_info(client, link, db_objects):
    artist_infos = client.fetch_artist_infos(link)
    return {
        'id': artist_infos['id'],
        'name': artist_infos['name'],
        'followers': artist_infos['followers']['total'],
        'popularity': artist_infos['popularity'],
        'images': [
            get_or_create(
                image['url'],
                db_objects,
                Image,
                {'url': image['url'], 'height': image['height'], 'width': image['width']}
            ) for image in artist_infos['images']],
        'genres': [
            get_or_create(
                genre,
                db_objects,
                Genre,
                {'name': genre}
            ) for genre in artist_infos['genres']],
    }


@shared_task
def sync_new_releases():
    client = SpotifyClient()
    if client.token is None:
        raise UnauthorizedException(
            f'Client must first authorize app to access his spotify account.'
            f'Aborting sync.'
        )

    releases = client.fetch_new_releases()
    albums = releases['albums']['items']

    db_objects = {
        'Genre': {},
        'Image': {},
    }
    artists_link = []
    artists = []

    for album in albums:
        artists_link.extend([artist['href'] for artist in album['artists']])
    for link in artists_link:
        artists.append(serialize_info(client, link, db_objects))

    serializer = ArtistSerializer(data=artists, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.create(artists)
