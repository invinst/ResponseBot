from __future__ import absolute_import

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
                stream.filter(follow=self.filter.follow, track=self.filter.track)
            except TweepError as e:
                if 'Stream object already connected!' in e.reason or \
                        'Wrong number of locations points' in e.reason:
                    raise APIError(e.reason)
