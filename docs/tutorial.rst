..
   Copyright 2016 Invisible Institute
   
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
   
       http://www.apache.org/licenses/LICENSE-2.0
   
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

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

Handler
-------

To receive an incoming tweet, you need to subclass :code:`BaseTweetHandler` and implement the :code:`on_tweet` method

.. code-block:: python

   class MyTweetHandler(BaseTweetHandler):
       def on_tweet(self, tweet):
           print('Received tweet: %s from %s' % (tweet.text, tweet.user.screen_name))

See what :code:`tweet` object contains in `reference <reference/responsebot.models.html#Tweet>`_.

Client
------

If your application want to post a reply to the received tweet, you can use ResponseBot's Twitter client to do so:

.. code-block:: python

   class MyTweetHandler(BaseTweetHandler):
       def on_tweet(self, tweet):
           self.client.tweet('Howdy @%s' % tweet.user.screen_name)

The :code:`client` object can also retweet, get or delete a specific tweet by ID. See `reference <reference/responsebot.responsebot_client.html>`_.
