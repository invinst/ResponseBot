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

import logging

from responsebot.common.exceptions import UserHandlerError
from responsebot.models import TweetFilter


class ResponseBotListener(object):
    """
    Forward received tweets from :class:`~responsebot.responsebot_stream.ResponseBotStream`
    """
    def __init__(self, handler_classes, client):
        """
        Inits the listener and tries to create handler instances from discovered user's handler classes

        :param handler_classes: List of :class:`~responsebot.handlers.base.BaseTweetHandler`'s derived classes
        :param client: Some Twitter API client for authentication. E.g. :class:`~responsebot.tweet_client.TweetClient`
        """
        self.client = client
        self.handlers = []

        self.register_handlers(handler_classes)

    def register_handlers(self, handler_classes):
        """
        Create handlers from discovered handler classes

        :param handler_classes: List of :class:`~responsebot.handlers.base.BaseTweetHandler`'s derived classes
        """
        for handler_class in handler_classes:
            try:
                self.handlers.append(handler_class(client=self.client))
                logging.info('Successfully registered {handler_class}'.format(
                    handler_class=getattr(handler_class, '__name__', str(handler_class)))
                )
            except Exception as e:
                # Catch all exception from user handler
                raise UserHandlerError(user_exception=e)

    def on_tweet(self, tweet):
        """
        Callback to receive tweet from :class:`~responsebot.responsebot_stream.ResponseBotStream`. Tries to forward the
        received tweet to registered handlers.

        :param tweet: An object containing a tweet's text and metadata
        :type tweet: :class:`~responsebot.models.Tweet`
        :raises :class:`~responsebot.common.exceptions.UserHandlerError`: If there is some unknown
        error from a custom handler
        """
        logging.info(u'Received tweet: `{message}`'.format(message=tweet.text))

        for handler in self.handlers:
            if not handler.catch_self_tweets and self.is_self_tweet(tweet):
                continue

            if not handler.filter.match_tweet(tweet=tweet, user_stream=self.client.config.get('user_stream')):
                continue

            try:
                handler.on_tweet(tweet)
            except Exception as e:
                # Catch all exception from user handler
                raise UserHandlerError(user_exception=e)

    def is_self_tweet(self, tweet):
        return self.client.get_current_user().id == tweet.user.id

    def get_merged_filter(self):
        """
        Return merged filter from list of handlers

        :return: merged filter
        :rtype: :class:`~responsebot.models.TweetFilter`
        """
        track = set()
        follow = set()

        for handler in self.handlers:
            track.update(handler.filter.track)
            follow.update(handler.filter.follow)

        return TweetFilter(track=list(track), follow=list(follow))
