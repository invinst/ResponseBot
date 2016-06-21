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

from datetime import datetime
from tweepy.error import TweepError, RateLimitError

from responsebot.common.constants import TWITTER_TWEET_NOT_FOUND_ERROR, TWITTER_USER_NOT_FOUND_ERROR, \
    TWITTER_PAGE_DOES_NOT_EXISTS_ERROR, TWITTER_DELETE_OTHER_USER_TWEET, TWITTER_ACCOUNT_SUSPENDED_ERROR, \
    TWITTER_USER_IS_NOT_LIST_MEMBER_SUBSCRIBER
from responsebot.common.exceptions import APIError, APIQuotaError
from responsebot.responsebot_client import ResponseBotClient

try:
    from mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock


class TweetClientTestCase(TestCase):
    def setUp(self):
        self.real_client = MagicMock()
        self.config = MagicMock()
        self.client = ResponseBotClient(self.real_client, self.config)

    def test_post_new_tweet(self):
        self.real_client.update_status = MagicMock(return_value=MagicMock(_json={
            'some_key': 'some value',
        }))

        tweet = self.client.tweet('some text')

        self.real_client.update_status.assert_called_once_with(status='some text', in_reply_to_status_id=None)
        self.assertEqual(tweet.some_key, 'some value')

    def test_reply(self):
        self.real_client.update_status = MagicMock(return_value=MagicMock(_json={
            'some_key': 'some value',
        }))

        tweet = self.client.tweet('some text', in_reply_to=123)

        self.real_client.update_status.assert_called_once_with(status='some text', in_reply_to_status_id=123)
        self.assertEqual(tweet.some_key, 'some value')

    def test_post_new_tweet_exceed_character_limit(self):
        self.real_client.update_status = MagicMock(
            side_effect=TweepError(api_code=186, reason='Status is more than 140 characters.'))

        self.assertRaises(
            APIError,
            self.client.tweet,
            text="some text with more than Twitter's character limit"
        )

    def test_post_new_tweet_duplicated(self):
        self.real_client.update_status = MagicMock(
            side_effect=TweepError(api_code=187, reason='Status is a duplicate.'))

        self.assertRaises(
            APIError,
            self.client.tweet,
            text='some text'
        )

    def test_post_new_tweet_unknown_tweet_error(self):
        self.real_client.update_status = MagicMock(
            side_effect=TweepError(api_code=-1, reason='Unknown'))

        self.assertRaises(
            APIError,
            self.client.tweet,
            text='some text'
        )

    def test_get_tweet(self):
        self.real_client.get_status = MagicMock(return_value=MagicMock(_json={
            'some_key': 'some value',
        }))

        tweet = self.client.get_tweet(123)

        self.real_client.get_status.assert_called_once_with(id=123)
        self.assertEqual(tweet.some_key, 'some value')

    def test_get_non_existent_tweet(self):
        exception = TweepError(reason='some reason', api_code=TWITTER_TWEET_NOT_FOUND_ERROR)
        self.real_client.get_status = MagicMock(
            side_effect=exception
        )

        tweet = self.client.get_tweet(123)

        self.real_client.get_status.assert_called_once_with(id=123)
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

        self.real_client.get_user.assert_called_once_with(user_id=123)
        self.assertEqual(user.some_key, 'some value')

    def test_get_non_existent_user(self):
        exception = TweepError(reason='some reason', api_code=TWITTER_USER_NOT_FOUND_ERROR)
        self.real_client.get_user = MagicMock(
            side_effect=exception
        )

        user = self.client.get_user(123)

        self.real_client.get_user.assert_called_once_with(user_id=123)
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

        self.real_client.destroy_status.assert_called_once_with(id=123)
        self.assertTrue(result)

    def test_remove_non_existent_tweet(self):
        exception = TweepError(reason='some reason', api_code=TWITTER_PAGE_DOES_NOT_EXISTS_ERROR)
        self.real_client.destroy_status = MagicMock(
            side_effect=exception
        )

        result = self.client.remove_tweet(123)

        self.real_client.destroy_status.assert_called_once_with(id=123)
        self.assertFalse(result)

    def test_remove_others_tweet(self):
        exception = TweepError(reason='some reason', api_code=TWITTER_DELETE_OTHER_USER_TWEET)
        self.real_client.destroy_status = MagicMock(
            side_effect=exception
        )

        result = self.client.remove_tweet(123)

        self.real_client.destroy_status.assert_called_once_with(id=123)
        self.assertFalse(result)

    def test_remove_tweet_encounter_error(self):
        self.real_client.destroy_status = MagicMock(
            side_effect=TweepError(reason='some reason')
        )

        self.assertRaises(APIError, self.client.remove_tweet, 123)

    def test_retweet(self):
        self.real_client.retweet = MagicMock()

        result = self.client.retweet(123)

        self.real_client.retweet.assert_called_once_with(id=123)
        self.assertTrue(result)

    def test_retweet_non_existent_tweet(self):
        exception = TweepError(reason='some reason', api_code=TWITTER_PAGE_DOES_NOT_EXISTS_ERROR)
        self.real_client.retweet = MagicMock(side_effect=exception)

        result = self.client.retweet(123)

        self.real_client.retweet.assert_called_once_with(id=123)
        self.assertFalse(result)

    def test_retweet_encounter_error(self):
        self.real_client.retweet = MagicMock(
            side_effect=TweepError(reason='some reason')
        )

        self.assertRaises(APIError, self.client.retweet, 123)

    def test_follow_user(self):
        self.real_client.create_friendship = MagicMock(return_value=MagicMock(_json={'some_key': 'some value'}))

        user = self.client.follow(123, notify=True)

        self.real_client.create_friendship.assert_called_once_with(user_id=123, follow=True)
        self.assertEqual(user.some_key, 'some value')

    def test_follow_user_403(self):
        self.real_client.create_friendship = MagicMock(side_effect=TweepError(reason='some reason',
                                                                              api_code=TWITTER_ACCOUNT_SUSPENDED_ERROR))
        self.real_client.get_user = MagicMock(return_value=MagicMock(_json={'some_key': 'some value'}))

        user = self.client.follow(123, notify=True)

        self.real_client.create_friendship.assert_called_once_with(user_id=123, follow=True)
        self.assertEqual(user.some_key, 'some value')

    def test_follow_user_unknown_exception(self):
        self.real_client.create_friendship = MagicMock(side_effect=TweepError(reason='unknown'))

        self.assertRaises(APIError, self.client.follow, 123)

    def test_unfollow_user(self):
        self.real_client.destroy_friendship = MagicMock(return_value=MagicMock(_json={'some_key': 'some value'}))

        user = self.client.unfollow(123)

        self.real_client.destroy_friendship.assert_called_once_with(user_id=123)
        self.assertEqual(user.some_key, 'some value')

    def test_unfollow_non_existent_user(self):
        self.real_client.destroy_friendship = MagicMock(side_effect=TweepError(reason='page not exists', api_code=34))

        self.assertRaises(APIError, self.client.unfollow, 123)

    def test_create_list(self):
        api_return = self.check_api_call_success(
            api='create_list',
            params={'name': 'some list'},
            mock_api='create_list',
            mock_api_params={
                'name': 'some list',
                'mode': 'public',
                'description': None
            },
            mock_api_return=MagicMock(
                something='something else',
                _api='api',
                created_at=datetime.now(),
                user=MagicMock()
            )
        )
        self.assertEqual(api_return.something, 'something else')

        self.check_api_call_errors(api='create_list', params={'name': 'some list'}, mock_api='create_list')

    def test_destroy_list(self):
        api_return = self.check_api_call_success(
            api='destroy_list',
            params={'list_id': 123},
            mock_api='destroy_list',
            mock_api_params={'list_id': 123},
            mock_api_return=MagicMock(
                something='something else',
                _api='api',
                created_at=datetime.now(),
                user=MagicMock()
            )
        )
        self.assertEqual(api_return.something, 'something else')

        self.check_api_call_errors(api='destroy_list', params={'list_id': 123}, mock_api='destroy_list')

    def test_update_list(self):
        api_return = self.check_api_call_success(
            api='update_list',
            params={'list_id': 123, 'name': 'new name'},
            mock_api='update_list',
            mock_api_params={
                'list_id': 123,
                'name': 'new name',
                'mode': None,
                'description': None
            },
            mock_api_return=MagicMock(
                something='something else',
                _api='api',
                created_at=datetime.now(),
                user=MagicMock()
            )
        )
        self.assertEqual(api_return.something, 'something else')

        self.check_api_call_errors(api='update_list', params={
            'list_id': 123,
            'name': 'new name'
        }, mock_api='update_list')

    def test_lists(self):
        api_return = self.check_api_call_success(
            api='lists',
            params={},
            mock_api='lists_all',
            mock_api_params={},
            mock_api_return=[MagicMock(
                something='something else',
                _api='api',
                created_at=datetime.now(),
                user=MagicMock()
            )]
        )
        self.assertEqual(api_return[0].something, 'something else')

        self.check_api_call_errors(api='lists', params={}, mock_api='lists_all')

    def test_lists_memberships(self):
        api_return = self.check_api_call_success(
            api='lists_memberships',
            params={},
            mock_api='lists_memberships',
            mock_api_params={},
            mock_api_return=[MagicMock(
                something='something else',
                _api='api',
                created_at=datetime.now(),
                user=MagicMock()
            )]
        )
        self.assertEqual(api_return[0].something, 'something else')

        self.check_api_call_errors(api='lists_memberships', params={}, mock_api='lists_memberships')

    def test_lists_subscriptions(self):
        api_return = self.check_api_call_success(
            api='lists_subscriptions',
            params={},
            mock_api='lists_subscriptions',
            mock_api_params={},
            mock_api_return=[MagicMock(
                something='something else',
                _api='api',
                created_at=datetime.now(),
                user=MagicMock()
            )]
        )
        self.assertEqual(api_return[0].something, 'something else')

        self.check_api_call_errors(api='lists_subscriptions', params={}, mock_api='lists_subscriptions')

    def test_list_timeline(self):
        api_return = self.check_api_call_success(
            api='list_timeline',
            params={'list_id': 123},
            mock_api='list_timeline',
            mock_api_params={'list_id': 123, 'since_id': None, 'max_id': None, 'count': 20},
            mock_api_return=[MagicMock(_json={'something': 'something else'})]
        )
        self.assertEqual(api_return[0].something, 'something else')

        self.check_api_call_errors(api='list_timeline', params={'list_id': 123}, mock_api='list_timeline')

    def test_get_list(self):
        api_return = self.check_api_call_success(
            api='get_list',
            params={'list_id': 123},
            mock_api='get_list',
            mock_api_params={'list_id': 123},
            mock_api_return=MagicMock(
                something='something else',
                _api='api',
                created_at=datetime.now(),
                user=MagicMock()
            )
        )
        self.assertEqual(api_return.something, 'something else')

        self.check_api_call_errors(api='get_list', params={'list_id': 123}, mock_api='get_list')

    def test_add_list_member(self):
        api_return = self.check_api_call_success(
                api='add_list_member',
                params={'list_id': 123, 'user_id': 456},
                mock_api='add_list_member',
                mock_api_params={'list_id': 123, 'user_id': 456},
                mock_api_return=MagicMock(
                    something='something else',
                    _api='api',
                    created_at=datetime.now(),
                    user=MagicMock())
        )
        self.assertEqual(api_return.something, 'something else')

        self.check_api_call_errors(api='add_list_member', params={'list_id': 123, 'user_id': 456},
                                   mock_api='add_list_member')

    def test_remove_list_member(self):
        api_return = self.check_api_call_success(
            api='remove_list_member',
            params={'list_id': 123, 'user_id': 456},
            mock_api='remove_list_member',
            mock_api_params={'list_id': 123, 'user_id': 456},
            mock_api_return=MagicMock(
                something='something else',
                _api='api',
                created_at=datetime.now(),
                user=MagicMock())
        )
        self.assertEqual(api_return.something, 'something else')

        self.check_api_call_errors(api='remove_list_member', params={'list_id': 123, 'user_id': 456},
                                   mock_api='remove_list_member')

    def test_list_members(self):
        api_return = self.check_api_call_success(
            api='list_members',
            params={'list_id': 123},
            mock_api='list_members',
            mock_api_params={'list_id': 123},
            mock_api_return=[MagicMock(_json={
                'something': 'something else'})]
        )
        self.assertEqual(api_return[0].something, 'something else')

        self.check_api_call_errors(api='list_members', params={'list_id': 123},
                                   mock_api='list_members')

    def test_is_list_member(self):
        api_return = self.check_api_call_success(
            api='is_list_member',
            params={'list_id': 123, 'user_id': 456},
            mock_api='show_list_member',
            mock_api_params={'list_id': 123, 'user_id': 456},
            mock_api_return=MagicMock()
        )
        self.assertEqual(api_return, True)

        api_return = self.check_api_call_success(
            api='is_list_member',
            params={'list_id': 123, 'user_id': 456},
            mock_api='show_list_member',
            mock_api_params={'list_id': 123, 'user_id': 456},
            mock_api_return=None,
            mock_api_effect=TweepError(api_code=TWITTER_USER_IS_NOT_LIST_MEMBER_SUBSCRIBER, reason='unknown')
        )
        self.assertEqual(api_return, False)

        self.check_api_call_errors(api='is_list_member', params={'list_id': 123, 'user_id': 456},
                                   mock_api='show_list_member')

    def test_subscribe_list(self):
        api_return = self.check_api_call_success(
            api='subscribe_list',
            params={'list_id': 123},
            mock_api='subscribe_list',
            mock_api_params={'list_id': 123},
            mock_api_return=MagicMock(
                something='something else',
                _api='api',
                created_at=datetime.now(),
                user=MagicMock()
            )
        )
        self.assertEqual(api_return.something, 'something else')

        self.check_api_call_errors(api='subscribe_list', params={'list_id': 123},
                                   mock_api='subscribe_list')

    def test_unsubscribe_list(self):
        api_return = self.check_api_call_success(
            api='unsubscribe_list',
            params={'list_id': 123},
            mock_api='unsubscribe_list',
            mock_api_params={'list_id': 123},
            mock_api_return=MagicMock(
                something='something else',
                _api='api',
                created_at=datetime.now(),
                user=MagicMock()
            )
        )
        self.assertEqual(api_return.something, 'something else')

        self.check_api_call_errors(api='unsubscribe_list', params={'list_id': 123},
                                   mock_api='unsubscribe_list')

    def test_list_subscribers(self):
        api_return = self.check_api_call_success(
            api='list_subscribers',
            params={'list_id': 123},
            mock_api='list_subscribers',
            mock_api_params={'list_id': 123},
            mock_api_return=[MagicMock(_json={'something': 'something else'})]
        )
        self.assertEqual(api_return[0].something, 'something else')

        self.check_api_call_errors(api='list_subscribers', params={'list_id': 123},
                                   mock_api='list_subscribers')

    def test_is_subscribed_list(self):
        api_return = self.check_api_call_success(
            api='is_subscribed_list',
            params={'list_id': 123, 'user_id': 456},
            mock_api='show_list_subscriber',
            mock_api_params={'list_id': 123, 'user_id': 456},
            mock_api_return=MagicMock()
        )
        self.assertEqual(api_return, True)

        api_return = self.check_api_call_success(
            api='is_subscribed_list',
            params={'list_id': 123, 'user_id': 456},
            mock_api='show_list_subscriber',
            mock_api_params={'list_id': 123, 'user_id': 456},
            mock_api_return=None,
            mock_api_effect=TweepError(api_code=TWITTER_USER_IS_NOT_LIST_MEMBER_SUBSCRIBER, reason='unknown')
        )
        self.assertEqual(api_return, False)

        self.check_api_call_errors(api='is_subscribed_list', params={'list_id': 123, 'user_id': 456},
                                   mock_api='show_list_subscriber')

    def check_api_call_errors(self, api, params, mock_api):
        setattr(self.real_client, mock_api, MagicMock(side_effect=TweepError(reason='unknown')))
        self.assertRaises(APIError, getattr(self.client, api), **params)

        setattr(self.real_client, mock_api, MagicMock(side_effect=RateLimitError(reason='unknown')))
        self.assertRaises(APIQuotaError, getattr(self.client, api), **params)

    def check_api_call_success(self, api, params, mock_api, mock_api_params, mock_api_return, mock_api_effect=None):
        if not mock_api_effect:
            setattr(self.real_client, mock_api, MagicMock(return_value=mock_api_return))
        else:
            setattr(self.real_client, mock_api, MagicMock(side_effect=mock_api_effect))

        try:
            api_return = getattr(self.client, api)(**params)

            getattr(self.real_client, mock_api).assert_called_once_with(**mock_api_params)

            return api_return
        except (APIError, APIQuotaError):
            self.fail('Expect no API error or API quota error')
