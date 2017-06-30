# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mock import patch, MagicMock

from django.test import TestCase

from demo.api import MarvelAPIWrapper
from demo.models import Character, RecentSearches, CharacterPhotos

FIXTURE_SEARCH_BY_QUERY = {
    u'status': u'Ok',
    u'code': 200,
    u'copyright': u'\xa9 2017 MARVEL',
    u'attributionText': u'Data provided by Marvel. \xa9 2017 MARVEL',
    u'etag': u'63cf0f02b30c0d640045f2713b4c9b7cb6c7c742',
    u'attributionHTML': u'<a href="http://marvel.com">Data provided by Marvel. \xa9 2017 MARVEL</a>',
    u'data': {
        u'count': 13, u'total': 13, u'limit': 20, u'results': [
            {
                u'resourceURI': u'http://gateway.marvel.com/v1/public/characters/1009610',
                u'description': u'Bitten by a radioactive spider, high school student Peter Parker gained the speed, strength and powers of a spider. Adopting the name Spider-Man, Peter hoped to start a career using his new abilities. Taught that with great power comes great responsibility, Spidey has vowed to use his powers to help people.',
                u'comics': {
                    u'available': 2973, u'items': [
                        {u'resourceURI': u'http://gateway.marvel.com/v1/public/comics/60151', u'name': u'A Year of Marvels (Trade Paperback)'}
                    ],
                    u'returned': 20, u'collectionURI': u'http://gateway.marvel.com/v1/public/characters/1009610/comics'
                },
                u'series': {
                    u'available': 639, u'items': [
                        {u'resourceURI': u'http://gateway.marvel.com/v1/public/series/22102', u'name': u'A Year of Marvels (2017)'}
                    ],
                    u'returned': 20, u'collectionURI': u'http://gateway.marvel.com/v1/public/characters/1009610/series'
                },
                u'modified': u'2016-09-28T12:15:21-0400',
                u'id': 1009610,
                u'stories': {
                    u'available': 4696, u'items': [
                        {u'resourceURI': u'http://gateway.marvel.com/v1/public/stories/483', u'type': u'interiorStory', u'name': u'Interior #483'}
                    ],
                    u'returned': 20, u'collectionURI': u'http://gateway.marvel.com/v1/public/characters/1009610/stories'
                },
                u'urls': [
                    {u'url': u'http://marvel.com/characters/54/spider-man?utm_campaign=apiRef&utm_source=e22432102dc5e7a392c8d26f7ccda6f6', u'type': u'detail'}
                ],
                u'events': {
                    u'available': 32, u'items': [
                        {u'resourceURI': u'http://gateway.marvel.com/v1/public/events/116', u'name': u'Acts of Vengeance!'}
                    ],
                    u'returned': 20, u'collectionURI': u'http://gateway.marvel.com/v1/public/characters/1009610/events'
                },
                u'thumbnail': {
                    u'path': u'http://i.annihil.us/u/prod/marvel/i/mg/3/50/526548a343e4b', u'extension': u'jpg'
                },
                u'name': u'Spider-Man'
            }
        ],
        u'offset': 0
    }
}

FIXTURE_SEARCH_BY_ID = {
    u'status': u'Ok', u'code': 200, u'copyright': u'\xa9 2017 MARVEL',
    u'attributionText': u'Data provided by Marvel. \xa9 2017 MARVEL',
    u'etag': u'5f597e9196d834cbbeed4546ffbe3aa33cb95b2f',
    u'attributionHTML': u'<a href="http://marvel.com">Data provided by Marvel. \xa9 2017 MARVEL</a>',
    u'data': {
        u'count': 1, u'total': 1, u'limit': 20, u'results': [
            {
                u'resourceURI': u'http://gateway.marvel.com/v1/public/characters/1009610',
                u'description': u'Bitten by a radioactive spider, high school student Peter Parker gained the speed, strength and powers of a spider. Adopting the name Spider-Man, Peter hoped to start a career using his new abilities. Taught that with great power comes great responsibility, Spidey has vowed to use his powers to help people.',
                u'comics': {
                    u'available': 2973, u'items': [
                        {
                            u'resourceURI': u'http://gateway.marvel.com/v1/public/comics/60151',
                            u'name': u'A Year of Marvels (Trade Paperback)'
                        }
                    ],
                    u'returned': 20,
                    u'collectionURI': u'http://gateway.marvel.com/v1/public/characters/1009610/comics'
                },
                u'series': {
                    u'available': 639, u'items': [
                        {
                            u'resourceURI': u'http://gateway.marvel.com/v1/public/series/22102',
                            u'name': u'A Year of Marvels (2017)'
                        }
                    ],
                    u'returned': 20,
                    u'collectionURI': u'http://gateway.marvel.com/v1/public/characters/1009610/series'
                },
                u'modified': u'2016-09-28T12:15:21-0400',
                u'id': 1009610,
                u'stories': {
                    u'available': 4696, u'items': [
                        {
                            u'resourceURI': u'http://gateway.marvel.com/v1/public/stories/483',
                            u'type': u'interiorStory',
                            u'name': u'Interior #483'
                        },
                    ],
                    u'returned': 20,
                    u'collectionURI': u'http://gateway.marvel.com/v1/public/characters/1009610/stories'
                },
                u'urls': [
                        {
                            u'url': u'http://marvel.com/characters/54/spider-man?utm_campaign=apiRef&utm_source=e22432102dc5e7a392c8d26f7ccda6f6',
                            u'type': u'detail'
                        }
                ],
                u'events': {
                    u'available': 32, u'items': [
                        {
                             u'resourceURI': u'http://gateway.marvel.com/v1/public/events/116',
                             u'name': u'Acts of Vengeance!'
                        }
                    ],
                    u'returned': 20,
                    u'collectionURI': u'http://gateway.marvel.com/v1/public/characters/1009610/events'
                },
                u'thumbnail': {
                    u'path': u'http://i.annihil.us/u/prod/marvel/i/mg/3/50/526548a343e4b',
                    u'extension': u'jpg'
                }, u'name': u'Spider-Man'
            }
        ],
        u'offset': 0
    }
}


class SavingToCacheTest(TestCase):

    def test_that_a_query_result_saved_to_cache(self):
        MarvelAPIWrapper._save_character_results(FIXTURE_SEARCH_BY_QUERY, 'spider-man')
        print [(x.etag, x.search_query) for x in RecentSearches.objects.all()]
        print [(x.bio, x.character_id, x.name) for x in Character.objects.all()]

    def test_that_a_query_id_is_saved_to_cache(self):
        MarvelAPIWrapper._save_character_result(FIXTURE_SEARCH_BY_ID, 1009610)
        api_result = FIXTURE_SEARCH_BY_ID['data']['results'][0]
        character = Character.objects.all().first()
        self.assertEqual(character.character_id, api_result['id'])
        self.assertEqual(character.name, api_result['name'])


class MarvelAPITest(TestCase):

    @patch('demo.api.requests.get')
    def test_that_a_query_is_handled_correct(self, requests_mock):
        api_response_mock = MagicMock()
        api_response_mock.status_code = 200
        api_response_mock.json.return_value = FIXTURE_SEARCH_BY_QUERY
        requests_mock.return_value = api_response_mock
        self.assertIsNone(RecentSearches.objects.all().first())
        MarvelAPIWrapper().search_character('spider-man')
        self.assertIsNotNone(RecentSearches.objects.all().first())

    @patch('demo.api.requests.get')
    def test_that_a_query_by_id_handled_correct(self, requests_mock):
        api_response_mock = MagicMock()
        api_response_mock.status_code = 200
        api_response_mock.json.return_value = FIXTURE_SEARCH_BY_ID
        requests_mock.return_value = api_response_mock
        self.assertIsNone(Character.objects.all().first())
        MarvelAPIWrapper().search_character_by_id(1009610)
        self.assertIsNotNone(Character.objects.all().first())

    @patch('demo.api.requests.get')
    def test_that_a_erroneous_response_is_handled_correct(self, requests_mock):
        api_response_mock = MagicMock()
        api_response_mock.status_code = 500
        api_response_mock.json.return_value = None
        requests_mock.return_value = api_response_mock
        self.assertIsNone(Character.objects.all().first())
        MarvelAPIWrapper().search_character_by_id(1009610)
        self.assertIsNone(Character.objects.all().first())

    @patch('demo.api.requests.get')
    def test_that_a_network_error_is_handled_correct(self, requests_mock):
        def side_effect():
            raise Exception('Network Error')
        requests_mock.side_effect = side_effect
        self.assertIsNone(Character.objects.all().first())
        response = MarvelAPIWrapper().search_character_by_id(1009610)
        self.assertIsNone(Character.objects.all().first())
        self.assertIsNone(response)
