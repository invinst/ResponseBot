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

from examples.handlers.save_tweet_handler import SaveTweetHandler
from responsebot.models import Tweet

try:
    from mock import MagicMock, patch, call
except ImportError:
    from unittest.mock import MagicMock, patch, call

from responsebot.responsebot_client import ResponseBotClient


class SaveTweetHandlerTestCase(TestCase):
    def test_save_incoming_tweets(self):
        tweet = Tweet({'text': '@bot mornin', 'user': {'screen_name': 'some_bloke'}})
        client = ResponseBotClient(
            client=MagicMock(me=MagicMock(return_value=MagicMock(_json={'id': 123}))),
            config=MagicMock()
        )
        mock_cursor = MagicMock()

        with patch('sqlite3.connect', return_value=MagicMock(cursor=MagicMock(return_value=mock_cursor))):
            handler = SaveTweetHandler(client)

            handler.on_tweet(tweet)

            mock_cursor.execute.assert_has_calls([
                call("CREATE TABLE IF NOT EXISTS tweets (tweet text, username text)"),
                call("INSERT INTO tweets VALUES ('@bot mornin', 'some_bloke')"),
            ])
