# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models





class Character(models.Model):
    bio = models.TextField(max_length=1000)
    character_id = models.IntegerField()
    is_popular = models.BooleanField(default=False)
    is_stale = models.BooleanField(default=True)


class RecentSearches(models.Model):
    results = models.IntegerField(default=0)
    search_query = models.TextField(max_length=150)
    characters = models.ManyToManyField(Character)

class CharacterPhotos(models.Model):
    character = models.ForeignKey(Character)
    image_url = models.TextField(max_length=150)


class Configuration(models.Model):
    code = models.TextField(max_length=4)
    value = models.TextField(max_length=20)
    description = models.TextField(max_length=150)

