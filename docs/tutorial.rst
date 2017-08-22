Tutorial
========

Authenticate
------------

ResponseBot uses Twitter API, which requires authentication. To do so, you need to register an application with Twitter
`here <https://apps.twitter.com/>`_. Twitter will provide your app with a consumer key & secret pair, you need to
generate an additional app token key & secret pair from your app management panel. After you have the credentials,
put it under the :code:`[auth]` section in the :code:`.responsebot` configuration file in your project root (or
whichever directory you run ResponseBot from).

.. code-block:: ini

   [auth]
   consumer_key = <consumer_key>
   consumer_secret = <consumer_secret>
   token_key = <token_key>
   token_secret = <token_secret>

If the credentials you provided are correct, when you run ResponseBot it should show like below

.. code-block:: bash

   $ start_responsebot --handlers-package <path_to_handler>
     [INFO] 2016-05-04 10:54:13 ResponseBot started
     [INFO] 2016-05-04 10:54:16 Successfully authenticated as <twitter_screen_name>

Otherwise it should show an error

.. code-block:: bash

     [ERROR] 2016-05-04 10:52:17 Could not authenticate.

You can pass the credentials as a :code:`start_responsebot`'s option instead of using a config file:

.. code-block:: bash

   $ start_responsebot --auth <consumer_key> <consumer_secret> <token_key> <token_secret>

Listen to public stream or user stream
--------------------------------------

The bot can listen to every tweets in the world (that match some keywords) or it can listen to its authenticated user's
timeline, as if it is that user. By default, the bot listen to the public stream, you can tell it to listen to the user
stream as follow:

.. code-block:: bash

   $ start_responsebot --user-stream

See more about stream and filters `here <guides/streams_and_filters.html>`_.

Handler
-------

To receive an incoming tweet, you need to subclass :code:`BaseTweetHandler` and implement the :code:`on_tweet` method.
You can specify what kind of tweets the bot should listen to by returning an appropriate
`TweetFilter <reference/responsebot.models.html#responsebot.models.TweetFilter>`_ in the :code:`get_filter` method.

.. code-block:: python

   class MyTweetHandler(BaseTweetHandler):
       def on_tweet(self, tweet):
           print('Received tweet: %s from %s' % (tweet.text, tweet.user.screen_name))

       def get_filter(self):
        return TweetFilter(track=['Donald Trump'], follow=['<your personal Twitter id>'])

See what :code:`tweet` object contains in `reference <reference/responsebot.models.html#responsebot.models.Tweet>`_.

If you're listening on user stream, you can catch non-tweet events (user following, etc.) as in
`this tutorial <guides/user_event_handling.html>`_.

Client
------

If your application want to post a reply to the received tweet, you can use ResponseBot's Twitter client to do so:

.. code-block:: python

   class MyTweetHandler(BaseTweetHandler):
       def on_tweet(self, tweet):
           self.client.tweet('Howdy @%s' % tweet.user.screen_name)

The :code:`client` object can also retweet, get or delete a specific tweet by ID. See `reference <reference/responsebot.responsebot_client.html>`_.
