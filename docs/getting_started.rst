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
       def on_tweet(self, tweet):
           print('Received tweet: %s from %s' % (tweet.text, tweet.user.screen_name))

Execute
~~~~~~~

.. code-block:: bash

   $ start_responsebot --handlers-package <python path to your package/module>

Test
~~~~

Send a tweet to the account which you used to create your Twitter application. You should see ResponseBot outputs

.. code-block:: bash

   Received tweet: <your tweet content> from <your sender tweet account>

Handler
-------
This is where you handle incoming tweet. For more information, see `handler reference <reference/responsebot.handlers.base.html>`_.

Client
------
We support a client to perform twitter actions like create, delete a tweet. For full list of supported actions, please look at the `client reference <reference/responsebot.responsebot_client.html>`_.
