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

"""
Entity classes for various entity types for ResponseBot
"""
from __future__ import absolute_import

from dateutil.parser import parse


class Tweet(object):
    """
    Represents a tweet. E.g. you can get a tweet's text via it's :code:`text` property (:code:`tweet.text`).
    All properties except :code:`retweeted_status`, :code:`quoted_status`, :code:`quoted_status_id_str`, :code:`in_reply_to_status_id`
    and :code:`in_reply_sto_status_id_str` have the same name as Twitter defined them `here <https://dev.twitter.com/overview/api/tweets>`_.
    :code:`retweeted_status` is renamed to :code:`retweeted_tweet`, similar for other properties above.
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
            elif key == 'quoted_status_id_str':
                setattr(self, 'quoted_tweet_id_str', value)
            elif key == 'in_reply_to_status_id':
                setattr(self, 'in_reply_to_tweet_id', value)
            elif key == 'in_reply_to_status_id_str':
                setattr(self, 'in_reply_to_tweet_id_str', value)
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


class TweetFilter(object):
    """
    Define criteria to filter tweets from Twitter's public stream. See `track` and `follow` parameters in `here <https://dev.twitter.com/streaming/overview/request-parameters>`_.
    """
    def __init__(self, track=[], follow=[]):
        """

        :param track: A list of keywords to follow (each could also be a @mention or a #hashtag)
        :param follow: A list of user ID strings to follow
        :return:
        """
        self.track = track
        self.follow = follow

    def match_tweet(self, tweet, user_stream):
        """
        Check if a tweet matches the defined criteria

        :param tweet: The tweet in question
        :type tweet: :class:`~responsebot.models.Tweet`
        :return: True if matched, False otherwise
        """
        if user_stream:
            if len(self.track) > 0:
                return self.is_tweet_match_track(tweet)

            return True
        else:
            return self.is_tweet_match_track(tweet) or self.is_tweet_match_follow(tweet)

    def is_tweet_match_track(self, tweet):
        tweet_text = tweet.text.lower()
        for value in self.track:
            if value.lower() in tweet_text:
                return True

        return False

    def is_tweet_match_follow(self, tweet):
        user_mentions = [x['id'] for x in tweet.entities.get('user_mentions', [])]
        for value in self.follow:
            int_value = int(value)
            if tweet.user.id == int_value or int_value in user_mentions:
                return True

        return False


class Event(object):
    """
    Represent a user events (e.g. following, unfollowing, etc.). See more `here <../guides/user_event_handling.html>`_
    and `here <https://dev.twitter.com/streaming/overview/messages-types#Events_event>`_.
    """
    def __init__(self, data):
        """
        :param data: Parsed JSON data
        :type data: dictionary
        """
        self.raw_data = data

        for key, value in data.items():
            if key == 'target':
                setattr(self, key, User(value))
            elif key == 'source':
                setattr(self, key, User(value))
            elif key == 'created_at':
                setattr(self, key, parse(value))
            else:
                setattr(self, key, value)

        setattr(self, 'target_object', self._parse_target_obj(data))

    def _parse_target_obj(self, data):
        # TODO: parse target obj base on event
        if data['event'] in ['follow', 'unfollow', 'block', 'unblock', 'user_update']:
            return None
        elif data['event'] in ['favorite', 'unfavorite', 'quoted_tweet']:
            return Tweet(data['target_object'])
        elif data['event'] in ['list_created', 'list_destroyed', 'list_updated', 'list_member_added',
                'list_member_removed', 'list_user_subscribed', 'list_user_unsubscribed']:
            return List(data['target_object'])
        return data.get('target_object')


class List(object):
    """
    Represent a user list.
    """
    def __init__(self, data):
        """
        :param data: Parsed JSON data
        :type data: dictionary
        """
        self.raw_data = data

        for key, value in data.items():
            if key == 'user':
                setattr(self, key, User(value))
            elif key == 'created_at':
                setattr(self, key, parse(value))
            else:
                setattr(self, key, value)
