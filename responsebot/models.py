"""
Entity classes for various entity types for ResponseBot
"""
from __future__ import absolute_import

from dateutil.parser import parse


class Tweet(object):
    """
    Represents a tweet. E.g. you can get a tweet's text via it's :code:`text` property (:code:`tweet.text`).
    All properties except :code:`retweeted_status` and :code:`quoted_status` have the same name as Twitter defined
    them `here <https://dev.twitter.com/overview/api/tweets>`_. :code:`retweeted_status` is renamed to
    :code:`retweeted_tweet` and :code:`quoted_status` is :code:`quoted_tweet`.
    """
    def __init__(self, data):
        """
        :param data: Parsed JSON data
        :type data: dictionary
        """
        self.raw_data = data

        # TODO: handle place. source, quoted_status_id_str
        for key, value in data.items():
            if key == 'user':
                setattr(self, key, User(value))
            elif key == 'created_at':
                setattr(self, key, parse(value))
            elif key == 'retweeted_status':
                setattr(self, 'retweeted_tweet', Tweet(value))
            elif key == 'quoted_status':
                setattr(self, 'quoted_tweet', Tweet(value))
            else:
                setattr(self, key, value)


class User(object):
    """
    Represents a user. E.g. you can get a user's screen name via it's :code:`screen_name` property
    (:code:`user.screen_name`). All properties except :code:`status` have the same name as Twitter defined them `here
    <https://dev.twitter.com/overview/api/users>`_. :code:`status` is renamed to :code:`tweet`.
    """
    def __init__(self, data):
        """
        :param data: Parsed JSON data
        :type data: dictionary
        """
        self.raw_data = data

        for key, value in data.items():
            if key == 'created_at':
                setattr(self, key, parse(value))
            elif key == 'status':
                setattr(self, 'tweet', Tweet(value))
            elif key == 'following':
                setattr(self, key, value is True)
            else:
                setattr(self, key, value)
