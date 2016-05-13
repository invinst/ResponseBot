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

from tweepy.error import TweepError

from responsebot.common.exceptions import AuthenticationError
from responsebot.responsebot_client import ResponseBotClient

try:
    from mock import patch, MagicMock
except ImportError:
    from unittest.mock import patch, MagicMock

from responsebot.utils import auth_utils


class AuthUtilsTestCase(TestCase):
    def test_failed_auth(self):
        with patch('responsebot.utils.auth_utils.tweepy.API.verify_credentials',
                   side_effect=TweepError(reason=[{'message': 'some message'}])):
            self.assertRaises(
                AuthenticationError,
                auth_utils.auth,
                consumer_key='ck', consumer_secret='cs', token_key='tk', token_secret='ts'
            )

    @patch('responsebot.utils.auth_utils.tweepy.API.verify_credentials')
    @patch('responsebot.utils.auth_utils.tweepy.API.me', return_value=MagicMock(screen_name='me'))
    def test_successful_auth(self, mock_me, mock_verify):
        try:
            client = auth_utils.auth(consumer_key='ck', consumer_secret='cs', token_key='tk', token_secret='ts')
        except AuthenticationError:
            self.fail('Expected no authentication error')
        else:
            self.assertIsInstance(client, ResponseBotClient)
