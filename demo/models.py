# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Character(models.Model):
    name = models.TextField(max_length=100)
    bio = models.TextField(max_length=1000)
    thumbnail = models.TextField(max_length=300)
    character_id = models.IntegerField()
    is_popular = models.BooleanField(default=False)
    is_stale = models.BooleanField(default=True)
    etag = models.TextField(max_length=100, default='')


class RecentSearches(models.Model):
    search_query = models.TextField(max_length=150)
    characters = models.ManyToManyField(Character)
    is_stale = models.BooleanField(default=False)
    etag = models.TextField(max_length=100)

    @property
    def results(self):
        return self.characters.all().count()


class CharacterPhotos(models.Model):
    character = models.ForeignKey(Character)
    image_url = models.TextField(max_length=150)


class Configuration(models.Model):
    code = models.TextField(max_length=4)
    value = models.TextField(max_length=20)
    description = models.TextField(max_length=150)

