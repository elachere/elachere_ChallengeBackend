# -*- coding: utf-8 -*-

from rest_framework.serializers import ListSerializer, Serializer

from .models import Artist


class ArtistListSerializer(ListSerializer):
    def create(self, validated_data):
        artists = []
        for item in validated_data:
            artist, _ = Artist.objects.update_or_create(
                id=item['id'],
                defaults={
                    'name': item['name'],
                    'followers': item['followers'],
                    'popularity': item['popularity'],
                }
            )
            artist.images.set(item['images'])
            artist.genres.set(item['genres'])
            artists.append(artist)
        return artists


class ArtistSerializer(Serializer):
    class Meta:
        list_serializer_class = ArtistListSerializer

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'followers': instance.followers,
            'popularity': instance.popularity,
            'images': [{
                'url': img.url,
                'width': img.width,
                'height': img.height
            } for img in instance.images.all()],
            'genres': [genre.name for genre in instance.genres.all()],
        }
