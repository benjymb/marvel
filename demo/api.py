import hashlib
from datetime import datetime

from django.conf import settings
import requests

from demo import models

class MarvelAPIWrapper(object):

    QUERY_CALL = 'characters?nameStartsWith={}&'
    QUERY_CALL_ID = 'characters/{}?'

    SEARCH_BY_QUERY = 0
    SEARCH_BY_ID = 1

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

    def _save_character_results(self, results, query):
        raise 'Not Implemented'

    def _make_api_call(self, type, value):
        query_call = self.QUERY_CALL
        if type == self.SEARCH_BY_ID:
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
            response_status = 500
            response = e.message
        return response_status, response

    def search_character(self, query):
        characters = None
        past_searches = models.RecentSearches.objects.filter(
            search_query__contains=query, is_stale=False
        )
        if past_searches.exists():
            characters = past_searches.characters__set.all()
        else:
            response, results = self._make_api_call(
                self.SEARCH_BY_QUERY, query
            )
            if response == 200:
                self._save_character_results(results, query)
                past_searches = models.RecentSearches.objects.filter(
                    search_query__contains=query, is_stale=False
                )
                if past_searches.exists():
                    characters = past_searches.characters__set.all()
        return characters









