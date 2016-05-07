from __future__ import absolute_import

from tweepy.error import TweepError

from responsebot.common.constants import TWITTER_PAGE_DOES_NOT_EXISTS_ERROR, TWITTER_TWEET_NOT_FOUND_ERROR, \
    TWITTER_USER_NOT_FOUND_ERROR, TWITTER_DELETE_OTHER_USER_TWEET
from responsebot.common.exceptions import APIError
from responsebot.models import Tweet, User


class ResponseBotClient(object):
    """
    Wrapper for all Twitter API clients.
    """
    def __init__(self, client):
        self._client = client
        self._current_user = None

    @property
    def tweepy_api(self):
        """
        Get the actual client object.

        :return: the actual client object
        """
        return self._client

    def get_current_user(self):
        if self._current_user is None:
            self._current_user = User(self._client.me()._json)
        return self._current_user

    def tweet(self, text):
        """
        Post a new tweet.

        :param text: the text to post
        :return: Tweet object
        """
        return Tweet(self._client.update_status(text)._json)

    def retweet(self, id):
        """
        Retweet a tweet.

        :param id: ID of the tweet in question
        :return: True if success, False otherwise
        """
        try:
            self._client.retweet(id)
            return True
        except TweepError as e:
            if e.api_code == TWITTER_PAGE_DOES_NOT_EXISTS_ERROR:
                return False
            raise APIError(str(e))

    def get_tweet(self, id):
        """
        Get an existing tweet.

        :param id: ID of the tweet in question
        :return: Tweet object. None if not found
        """
        try:
            return Tweet(self._client.get_status(id)._json)
        except TweepError as e:
            if e.api_code == TWITTER_TWEET_NOT_FOUND_ERROR:
                return None
            raise APIError(str(e))

    def get_user(self, id):
        """
        Get a user's info.

        :param id: ID of the user in question
        :return: User object. None if not found
        """
        try:
            return User(self._client.get_user(id)._json)
        except TweepError as e:
            if e.api_code == TWITTER_USER_NOT_FOUND_ERROR:
                return None
            raise APIError(str(e))

    def remove_tweet(self, id):
        """
        Delete a tweet.

        :param id: ID of the tweet in question
        :return: True if success, False otherwise
        """
        try:
            self._client.destroy_status(id)
            return True
        except TweepError as e:
            if e.api_code in [TWITTER_PAGE_DOES_NOT_EXISTS_ERROR, TWITTER_DELETE_OTHER_USER_TWEET]:
                return False
            raise APIError(str(e))
