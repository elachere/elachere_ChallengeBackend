# -*- coding: utf-8 -*-
from celery import shared_task

from .client import SpotifyClient
from .models import Artist, Genre, Image
from .serializers import ArtistSerializer


def serialize_info(client, link):
    artist_infos = client.fetch_artist_infos(link)
    return {
        'id': artist_infos['id'],
        'name': artist_infos['name'],
        'followers': artist_infos['followers']['total'],
        'popularity': artist_infos['popularity'],
        'images': [Image.objects.get_or_create(url=image['url']) for image in artist_infos['images']],
        'genres': [Genre.objects.get_or_create(name=genre) for genre in artist_infos['genres']]
    }


@shared_task
def sync_new_releases():
    client = SpotifyClient()
    releases = client.fetch_new_releases()
    albums = releases['albums']['items']

    artists_link = []
    artists = []

    for album in albums:
        artists_link.extend([artist['href'] for artist in album['artists']])
    for link in artists_link:
        artists.append(serialize_info(client, link))

    serializer = ArtistSerializer(artists, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.create(artists)
