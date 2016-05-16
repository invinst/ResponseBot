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

from responsebot.common.constants import TWITTER_TWEET_NOT_FOUND_ERROR, TWITTER_USER_NOT_FOUND_ERROR, \
    TWITTER_PAGE_DOES_NOT_EXISTS_ERROR, TWITTER_DELETE_OTHER_USER_TWEET
from responsebot.common.exceptions import APIError
from responsebot.responsebot_client import ResponseBotClient

try:
    from mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock


class TweetClientTestCase(TestCase):
    def setUp(self):
        self.real_client = MagicMock()
        self.client = ResponseBotClient(self.real_client)

    def test_post_new_tweet(self):
        self.real_client.update_status = MagicMock(return_value=MagicMock(_json={
            'some_key': 'some value',
        }))

        tweet = self.client.tweet('some text')

        self.real_client.update_status.assert_called_once_with('some text')
        self.assertEqual(tweet.some_key, 'some value')

    def test_get_tweet(self):
        self.real_client.get_status = MagicMock(return_value=MagicMock(_json={
            'some_key': 'some value',
        }))

        tweet = self.client.get_tweet(123)

        self.real_client.get_status.assert_called_once_with(123)
        self.assertEqual(tweet.some_key, 'some value')

    def test_get_non_existent_tweet(self):
        exception = TweepError(reason='some reason', api_code=TWITTER_TWEET_NOT_FOUND_ERROR)
        self.real_client.get_status = MagicMock(
            side_effect=exception
        )

        tweet = self.client.get_tweet(123)

        self.real_client.get_status.assert_called_once_with(123)
        self.assertIsNone(tweet)

    def test_get_tweet_encounter_error(self):
        self.real_client.get_status = MagicMock(
            side_effect=TweepError(reason='some reason')
        )

        self.assertRaises(APIError, self.client.get_tweet, 123)

    def test_get_user(self):
        self.real_client.get_user = MagicMock(return_value=MagicMock(_json={
            'some_key': 'some value',
        }))

        user = self.client.get_user(123)

        self.real_client.get_user.assert_called_once_with(123)
        self.assertEqual(user.some_key, 'some value')

    def test_get_non_existent_user(self):
        exception = TweepError(reason='some reason', api_code=TWITTER_USER_NOT_FOUND_ERROR)
        self.real_client.get_user = MagicMock(
            side_effect=exception
        )

        user = self.client.get_user(123)

        self.real_client.get_user.assert_called_once_with(123)
        self.assertIsNone(user)

    def test_get_user_encounter_error(self):
        self.real_client.get_user = MagicMock(
            side_effect=TweepError(reason='some reason')
        )

        self.assertRaises(APIError, self.client.get_user, 123)

    def test_get_current_user(self):
        self.real_client.me = MagicMock(return_value=MagicMock(_json={
            'some_key': 'some value',
        }))

        user = self.client.get_current_user()

        self.real_client.me.assert_called_once_with()
        self.assertEqual(user.some_key, 'some value')

    def test_cache_current_user(self):
        self.real_client.me = MagicMock()

        self.client.get_current_user()
        self.client.get_current_user()

        self.assertEqual(self.real_client.me.call_count, 1)

    def test_remove_tweet(self):
        self.real_client.destroy_status = MagicMock()

        result = self.client.remove_tweet(123)

        self.real_client.destroy_status.assert_called_once_with(123)
        self.assertTrue(result)

    def test_remove_non_existent_tweet(self):
        exception = TweepError(reason='some reason', api_code=TWITTER_PAGE_DOES_NOT_EXISTS_ERROR)
        self.real_client.destroy_status = MagicMock(
            side_effect=exception
        )

        result = self.client.remove_tweet(123)

        self.real_client.destroy_status.assert_called_once_with(123)
        self.assertFalse(result)

    def test_remove_others_tweet(self):
        exception = TweepError(reason='some reason', api_code=TWITTER_DELETE_OTHER_USER_TWEET)
        self.real_client.destroy_status = MagicMock(
            side_effect=exception
        )

        result = self.client.remove_tweet(123)

        self.real_client.destroy_status.assert_called_once_with(123)
        self.assertFalse(result)

    def test_remove_tweet_encounter_error(self):
        self.real_client.destroy_status = MagicMock(
            side_effect=TweepError(reason='some reason')
        )

        self.assertRaises(APIError, self.client.remove_tweet, 123)

    def test_retweet(self):
        self.real_client.retweet = MagicMock()

        result = self.client.retweet(123)

        self.real_client.retweet.assert_called_once_with(123)
        self.assertTrue(result)

    def test_retweet_non_existent_tweet(self):
        exception = TweepError(reason='some reason', api_code=TWITTER_PAGE_DOES_NOT_EXISTS_ERROR)
        self.real_client.retweet = MagicMock(side_effect=exception)

        result = self.client.retweet(123)

        self.real_client.retweet.assert_called_once_with(123)
        self.assertFalse(result)

    def test_retweet_encounter_error(self):
        self.real_client.retweet = MagicMock(
            side_effect=TweepError(reason='some reason')
        )

        self.assertRaises(APIError, self.client.retweet, 123)
