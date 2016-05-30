User event handling
===================

If you're listening to `user stream <streams_and_filters.html>`_, you can catch non-tweet events (user following, etc.)
by subclassing the `BaseEventHandler <../reference/responsebot.handlers.event.html#Event>`_ class and set it in your tweet handler, as follow:

.. code-block:: python

   class MyEventHandler(BaseEventHandler):
       def on_follow(self, event):
           pass

       def handle(self, event):
           super(MyEventHandler, self).handle(event)
           # do sth


   class MyTweetHandler(BaseTweetHandler):
       event_handler_class = MyEventHandler

Currently we support callbacks :code:`on_<event>` so you can easily implementing them. You can override :code:`handle` for more customization if needed.

For a list of Twitter user events, visit `this docs <https://dev.twitter.com/streaming/overview/messages-types#Events_event>`_.
