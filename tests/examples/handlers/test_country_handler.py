# Copyright 2016 Invisible Institute
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest.case import TestCase

try:
    from mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock

from examples.handlers.country_handler import CountryHandler
from responsebot.models import Tweet
from responsebot.responsebot_client import ResponseBotClient


class CountryHandlerTestCase(TestCase):
    def test_reply_country_info(self):
        client = MagicMock(tweet=MagicMock())
        handler = CountryHandler(client)
        tweet = Tweet({'text': '@bot Andorra'})

        handler.on_tweet(tweet)

        client.tweet.assert_called_once_with(
            'Country: Andorra\n'
            'Population: 84000\n'
            'Languages: ca\n'
            'Continent: Europe'
        )

    def test_does_not_reply_non_existent_country(self):
        client = MagicMock(tweet=MagicMock())
        handler = CountryHandler(client)
        tweet = Tweet({'text': '@bot Azeroth'})

        handler.on_tweet(tweet)

        client.tweet.assert_not_called()
