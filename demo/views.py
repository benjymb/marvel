# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView, View

from demo.api import MarvelAPIWrapper
from demo.models import RecentSearches, Character

def characters_serializer(queryset):
    return json.dumps([{
            'name': x.name,
            'thumbnail': x.thumbnail,
            'character_id': x.character_id
        } for x in queryset])

def character_serializer(character):
    return json.dumps({
            'name': character.name,
            'description': character.bio,
            'thumbnail': character.thumbnail,
            'character_id': character.character_id
        })

class IndexPage(TemplateView):

    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        return super(IndexPage, self).dispatch(request, *args, **kwargs)


class QueryCharactersView(View):

    def dispatch(self, request, *args, **kwargs):
        return super(QueryCharactersView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        results = MarvelAPIWrapper().search_character(request.GET['query'])
        data = characters_serializer(results)
        return HttpResponse(data, content_type='application/json')


class CharacterView(View):

    def dispatch(self, request, *args, **kwargs):
        return super(CharacterView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        result = MarvelAPIWrapper().search_character_by_id(request.GET['character_id'])
        data = character_serializer(result)
        return HttpResponse(data, content_type='application/json')


class MostPopularView(View):

    def dispatch(self, request, *args, **kwargs):
        return super(MostPopularView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        results = Character.objects.filter(is_popular=True)
        data = characters_serializer(results)
        return HttpResponse(data, content_type='application/json')


class RecentView(View):

    def dispatch(self, request, *args, **kwargs):
        return super(RecentView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        results = RecentSearches.objects.latest('pk').characters.all()
        data = characters_serializer(results)
        return HttpResponse(data, content_type='application/json')