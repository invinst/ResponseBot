Streams and filters
===================

Streams
-------

Twitter has `three stream APIs <https://dev.twitter.com/streaming/overview>`_ to listen to. ResponseBot currently
implement the public stream and user stream listening methods. By default the bot listen to public stream, you can tell
the bot to listen to user stream by setting it in the config file:

.. code-block:: ini

   [stream]
   user_stream=true

or pass in a flag in the start command:

.. code-block:: bash

   $ start_responsebot --user-stream

Filters
-------

The public stream utilize two parameters: :code:`track` and :code:`follow`, to filter global streams (you cannot listen
to every tweets in the world, you must have either 1 keyword to track or 1 user to follow). You provide these parameters
in your handlers' :code:`get_filter` method as follow:

.. code-block:: python

   def get_filter(self):
       return TweetFilter(track=['keyword'], follow=['user_id'])

By default the `BaseTweetHandler <reference/responsebot.handlers.base.html#responsebot.handlers.base.BaseTweetHandler>`_
returns a filter with the :code:`follow` parameter set as the bot's authenticated user and an empty :code:`track`
parameter, which is equivalent to running the bot with :code:`user_stream` and provide no :code:`track` in your
handlers.

The :code:`follow` parameter will not be used if you use :code:`user_stream`. See more about
`TweetFilter <reference/responsebot.models.html#responsebot.models.TweetFilter>`_
