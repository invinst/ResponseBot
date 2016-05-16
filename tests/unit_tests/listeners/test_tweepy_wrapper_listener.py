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

from responsebot.listeners.tweepy_wrapper_listener import TweepyWrapperListener

try:
    from mock import MagicMock, patch
except ImportError:
    from unittest.mock import MagicMock, patch


class TweepyWrapperListenerTestCase(TestCase):
    def test_call_generic_listener_on_tweet(self):
        generic_listener = MagicMock(on_tweet=MagicMock())
        status = MagicMock(_json={'some key': 'some value'})

        tweet_obj = 'tweet_obj'
        with patch('responsebot.listeners.tweepy_wrapper_listener.Tweet', return_value=tweet_obj) as mock_tweet_obj:
            TweepyWrapperListener(listener=generic_listener).on_status(status)

            mock_tweet_obj.assert_called_once_with(status._json)
            generic_listener.on_tweet.assert_called_once_with(tweet_obj)
