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

class BaseEventHandler(object):
    """
    Abstract event handler. Read more about event `here <../guides/user_event_handling.html>`_ and `here <https://dev.twitter.com/streaming/overview/messages-types#Events_event>`_.
    """
    def __init__(self, client):
        """
        Init event handler.

        :param client: Some Twitter API client for authentication. E.g. :class:`~responsebot.tweet_client.TweetClient`
        """
        self.client = client

    def handle(self, event):
        """
        Entry point to handle user events.

        :param event: Received event. See a full list `here <https://dev.twitter.com/streaming/overview/messages-types#Events_event>`_.
        """
        callback = getattr(self, 'on_{event}'.format(event=event.event), None)
        callback(event)

    def on_access_revoked(self, event):
        """
        Event-specific callback for handling :code:`access_revoked` events. This will trigger when you deauthorize a
        stream. See more of this `here <https://dev.twitter.com/streaming/overview/messages-types#Events_event>`_

        :param event: Received event.
        :type event: :class:`~responsebot.models.Event`
        """
        pass

    def on_block(self, event):
        """
        Event-specific callback for handling :code:`block` events. This will trigger when you block someone.

        :param event: Received event.
        :type event: :class:`~responsebot.models.Event`
        """
        pass

    def on_unblock(self, event):
        """
        Event-specific callback for handling :code:`unblock` events. This will trigger when you unblock someone.

        :param event: Received event.
        :type event: :class:`~responsebot.models.Event`
        """
        pass

    def on_favorite(self, event):
        """
        Event-specific callback for handling :code:`favorite` events. This will trigger when someone like your
        tweet or you like someone's tweet.

        :param event: Received event.
        :type event: :class:`~responsebot.models.Event`
        """
        pass

    def on_unfavorite(self, event):
        """
        Event-specific callback for handling :code:`unfavorite` events. This will trigger when someone unlike your
        tweet or you unlike someone's tweet.

        :param event: Received event.
        :type event: :class:`~responsebot.models.Event`
        """
        pass

    def on_follow(self, event):
        """
        Event-specific callback for handling :code:`follow` events. This will trigger when someone follow the
        current user or when current user follow someone.

        :param event: Received event.
        :type event: :class:`~responsebot.models.Event`
        """
        pass

    def on_unfollow(self, event):
        """
        Event-specific callback for handling :code:`unfollow` events. This will trigger when you unfollow someone.

        :param event: Received event.
        :type event: :class:`~responsebot.models.Event`
        """
        pass

    def on_list_created(self, event):
        """
        Event-specific callback for handling :code:`list_created` events. This will trigger when you create a list.

        :param event: Received event.
        :type event: :class:`~responsebot.models.Event`
        """
        pass

    def on_list_destroyed(self, event):
        """
        Event-specific callback for handling :code:`list_destroyed` events. This will trigger when you delete your
        list.

        :param event: Received event.
        :type event: :class:`~responsebot.models.Event`
        """
        pass

    def on_list_updated(self, event):
        """
        Event-specific callback for handling :code:`list_updated` events. This will trigger when you update your list.

        :param event: Received event.
        :type event: :class:`~responsebot.models.Event`
        """
        pass

    def on_list_member_added(self, event):
        """
        Event-specific callback for handling :code:`list_member_added` events. This will trigger when you are added
        to a list or you add someone to your list.

        :param event: Received event.
        :type event: :class:`~responsebot.models.Event`
        """
        pass

    def on_list_member_removed(self, event):
        """
        Event-specific callback for handling :code:`list_member_removed` events. This will trigger when you are removed
        from a list or you remove someone from your list.

        :param event: Received event.
        :type event: :class:`~responsebot.models.Event`
        """
        pass

    def on_list_user_subscribed(self, event):
        """
        Event-specific callback for handling :code:`list_user_subscribed` events. This will trigger when your list
        is subscribed to or you subscribe to a list.

        :param event: Received event.
        :type event: :class:`~responsebot.models.Event`
        """
        pass

    def on_list_user_unsubscribed(self, event):
        """
        Event-specific callback for handling :code:`list_user_unsubscribed` events. This will trigger when your list
        is unsubscribed from or you unsubscribe from a list.

        :param event: Received event.
        :type event: :class:`~responsebot.models.Event`
        """
        pass

    def on_quoted_tweet(self, event):
        """
        Event-specific callback for handling :code:`quoted_tweet` events. This will trigger when someone quote your
        tweet.

        :param event: Received event.
        :type event: :class:`~responsebot.models.Event`
        """
        pass

    def on_user_update(self, event):
        """
        Event-specific callback for handling :code:`user_update` events. This will trigger when you update your profile
        or private tweets.

        :param event: Received event.
        :type event: :class:`~responsebot.models.Event`
        """
        pass
