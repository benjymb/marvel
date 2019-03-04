import hashlib
from datetime import datetime

from django.conf import settings
import requests

from demo import models


class DBFinder(object):

    @staticmethod
    def search_characters(query):
        characters = None
        past_searches = models.RecentSearches.objects.filter(
            search_query__contains=query, is_stale=False
        )
        if past_searches.exists():
            characters = past_searches.first().characters.all()
        return characters

    @staticmethod
    def search_character(character_id):
        return models.Character.objects.filter(
            character_id=character_id
        ).first()


class MarvelAPIWrapper(object):

    QUERY_CALL = 'characters?nameStartsWith={}&'
    QUERY_CALL_ID = 'characters/{}?'

    SEARCH_BY_QUERY = 0
    SEARCH_BY_ID = 1

    DEFAULT_API_RESPONSE_STATUS = 500

    def __init__(self):
        epoch = datetime(1970, 1, 1)
        public_key = settings.PUBLIC_MARVEL_KEY
        private_key = settings.PRIVATE_MARVEL_KEY
        timestamp = str(int((datetime.now() - epoch).total_seconds()))
        hashed_key = hashlib.md5(
            timestamp + private_key + public_key
        ).hexdigest()
        self.api_url = (
            settings.MARVEL_API_URL + '{}' +
            settings.MARVEL_SIGNING_FORMAT.format(
                timestamp, public_key, hashed_key
            )
        )

    @staticmethod
    def _save_character_results(results, query):
        previous_searches = models.RecentSearches.objects.filter(search_query=query)
        etag_changed = False
        was_stale = False
        is_new = False
        if not previous_searches.exists():
            recent_search = models.RecentSearches.objects.create(
                search_query=query, etag=results['etag']
            )
            characters = results['data']['results']
            for character in characters:
                thumbnail_photo = (
                    character['thumbnail']['path'] + '.' +
                    character['thumbnail']['extension']
                )
                new_character = models.Character.objects.create(
                    character_id=character['id'], bio=character['description'],
                    name=character['name'], thumbnail=thumbnail_photo
                )
                recent_search.characters.add(new_character)
                models.CharacterPhotos.objects.create(
                    character=new_character, image_url=thumbnail_photo
                )
        elif was_stale:
            previous_searches.update(is_stale=False)

    @staticmethod
    def _save_character_result(results, character_id):
        character = models.Character.objects.filter(
            character_id=character_id
        ).first()
        etag_changed = False
        was_stale = False
        is_new = False
        if not character:
                character_result = results['data']['results'][0]
                thumbnail_photo = (
                    character_result['thumbnail']['path'] + '.' +
                    character_result['thumbnail']['extension']
                )
                character = models.Character.objects.create(
                    character_id=character_id, bio=character_result['description'],
                    name=character_result['name'], thumbnail=thumbnail_photo,
                    etag=results['etag']
                )
                models.CharacterPhotos.objects.create(
                    character=character, image_url=thumbnail_photo
                )
        elif was_stale:
            character.is_stale = False
            character.save()

    def _make_api_call(self, query_type, value):
        query_call = self.QUERY_CALL
        if query_type == self.SEARCH_BY_ID:
            query_call = self.QUERY_CALL_ID
        try:
            api_response = requests.get(
                self.api_url.format(
                    query_call.format(value)
                )
            )
            response_status = api_response.status_code
            response = api_response.json()
        except Exception as e:
            response_status = self.DEFAULT_API_RESPONSE_STATUS
            response = e.message
        return response_status, response

    def search_character(self, query):
        characters = DBFinder.search_characters(query)
        if not characters:
            response, results = self._make_api_call(
                self.SEARCH_BY_QUERY, query
            )
            if response == 200:
                self._save_character_results(results, query)
                characters = DBFinder.search_characters(query)
        return characters

    def search_character_by_id(self, character_id):
        character = DBFinder.search_character(character_id)
        if not character:
            response, results = self._make_api_call(
                self.SEARCH_BY_ID, character_id
            )
            if response == 200:
                self._save_character_result(results, character_id)
                character = DBFinder.search_character(character_id)
        return character












