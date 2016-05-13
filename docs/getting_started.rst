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

Getting Started
===============

Introduction
------------
A framework to quickly develop listen-and-answer twitter bots. You can define multiple actions to be executed every time a tweet arrives.

Installation
------------
.. code-block:: bash

   $ pip install responsebot

Quick start
-----------
Authenticate
~~~~~~~~~~~~

Create a :code:`.responsebot` file in your project root with your Twitter API credentials (which can be obtained after you created a Twitter application `here <https://apps.twitter.com/>`_).

.. code-block:: ini

   [auth]
   consumer_key = <consumer_key>
   consumer_secret = <consumer_secret>
   token_key = <token_key>
   token_secret = <token_secret>

Create a handler
~~~~~~~~~~~~~~~~

.. code-block:: python

   from responsebot.handlers.base import BaseTweetHandler


   class MyTweetHandler(BaseTweetHandler):
       def get_filter(self):
           return TweetFilter(track=['Donald Trump'], follow=['<your personal Twitter id>'])

       def on_tweet(self, tweet):
           print('Received tweet: %s from %s' % (tweet.text, tweet.user.screen_name))

Execute
~~~~~~~

.. code-block:: bash

   $ start_responsebot --handlers-package <python path to your package/module>

Test
~~~~

The bot should now receive tweets containing 'Donald Trump' or tweets posted by you. You should see ResponseBot outputs

.. code-block:: bash

   Received tweet: <your tweet content> from <your sender tweet account>

Handler
-------
This is where you handle incoming tweet. For more information, see `handler reference <reference/responsebot.handlers.base.html>`_.

Client
------
We support a client to perform twitter actions like create, delete a tweet. For full list of supported actions, please look at the `client reference <reference/responsebot.responsebot_client.html>`_.
