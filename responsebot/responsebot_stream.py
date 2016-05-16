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

from __future__ import absolute_import

import logging

import tweepy
from tweepy.error import TweepError

from responsebot.common.exceptions import APIError
from responsebot.listeners.tweepy_wrapper_listener import TweepyWrapperListener


class ResponseBotStream(object):
    """
    Connect to Twitter's streaming API and handle any error that occurs.
    """
    def __init__(self, client, listener):
        """
        :param client: Some Twitter API client for authentication. E.g. :class:`~responsebot.tweet_client.TweetClient`
        :param listener: A central listener that will receive tweets from the stream and forward them to user's
        handlers. E.g. :class:`~responsebot.listeners.responsebot_listener.ResponseBotListener`
        """
        self.client = client
        self.listener = listener
        self.filter = listener.get_merged_filter()

    def start(self, retry_limit=None):
        """
        Try to connect to Twitter's streaming API.

        :param retry_limit: The maximum number of retries in case of failures. Default is None (unlimited)
        :raises :class:`~responsebot.common.exceptions.APIError`: If there's some critical API error
        """
        # Run tweepy stream
        wrapper_listener = TweepyWrapperListener(listener=self.listener)
        stream = tweepy.Stream(auth=self.client.tweepy_api.auth, listener=wrapper_listener)

        retry_counter = 0
        while retry_limit is None or retry_counter <= retry_limit:
            try:
                retry_counter += 1
                if not self.client.config.get('user_stream'):
                    logging.info('Listening to public stream')
                    stream.filter(follow=self.filter.follow, track=self.filter.track)
                else:
                    if self.filter.follow:
                        logging.warning('Follow filters won\'t be used in user stream')

                    logging.info('Listening to user stream')
                    stream.userstream(track=self.filter.track)
            except TweepError as e:
                if 'Stream object already connected!' in e.reason or \
                        'Wrong number of locations points' in e.reason:
                    raise APIError(e.reason)
            except AttributeError as e:
                # Known Tweepy's issue https://github.com/tweepy/tweepy/issues/576
                if '\'NoneType\' object has no attribute \'strip\'' in str(e):
                    pass
