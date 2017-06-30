# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView, View

from demo.api import MarvelAPIWrapper



class IndexPage(TemplateView):

    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        return super(IndexPage, self).dispatch(request, *args, **kwargs)


class QueryCharacter(View):

    def dispatch(self, request, *args, **kwargs):
        return super(QueryCharacter, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        results = MarvelAPIWrapper().search_character(request.GET['query'])
        data = json.dumps([{
            'name': x.name,
            'description': x.bio,
            'thumbnail': x.thumbnail
        } for x in results])
        return HttpResponse(data, content_type='application/json')

