from unittest.case import TestCase

from responsebot.listeners.responsebot_listener import ResponseBotListener

try:
    from mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock


class ResponseBotListenerTestCase(TestCase):
    def test_register_handlers(self):
        handler_class_1 = MagicMock(return_value='handler 1')
        handler_class_2 = MagicMock(return_value='handler 2')

        listener = ResponseBotListener(handler_classes=[handler_class_1, handler_class_2], client=MagicMock())

        self.assertEqual(listener.handlers, ['handler 1', 'handler 2'])

    def test_call_handlers_on_tweet(self):
        handler_1 = MagicMock(on_tweet=MagicMock())
        handler_2 = MagicMock(on_tweet=MagicMock())
        listener = ResponseBotListener(handler_classes=[], client=MagicMock())
        listener.handlers = [handler_1, handler_2]

        tweet = MagicMock(text='tweet')
        listener.on_tweet(tweet)

        handler_1.on_tweet.assert_called_once_with(tweet)
        handler_2.on_tweet.assert_called_once_with(tweet)

    def test_handlers_handle_self_tweets(self):
        ignore_own_tweet_handler = MagicMock(catch_self_tweets=False)
        not_ignore_own_tweet_handler = MagicMock(catch_self_tweets=True)

        client = MagicMock(get_current_user=MagicMock(return_value=MagicMock(id='responsebot')))
        listener = ResponseBotListener(handler_classes=[MagicMock], client=client)
        listener.handlers = [ignore_own_tweet_handler, not_ignore_own_tweet_handler]
        tweet = MagicMock(user=MagicMock(id='responsebot'))

        listener.on_tweet(tweet)

        not_ignore_own_tweet_handler.on_tweet.assert_called_once_with(tweet)
        ignore_own_tweet_handler.on_tweet.assert_not_called()

    def test_match_tweet_to_handler(self):
        matched_handler = MagicMock(filter=MagicMock(match_tweet=MagicMock(return_value=True)))
        unmatched_handler = MagicMock(filter=MagicMock(match_tweet=MagicMock(return_value=False)))

        listener = ResponseBotListener(handler_classes=[], client=MagicMock())
        listener.handlers = [matched_handler, unmatched_handler]

        tweet = MagicMock()

        listener.on_tweet(tweet)

        matched_handler.on_tweet.assert_called_once_with(tweet)
        unmatched_handler.on_tweet.assert_not_called()

    def test_call_handlers_on_event(self):
        handler_1 = MagicMock(on_event=MagicMock())
        handler_2 = MagicMock(on_event=MagicMock())
        listener = ResponseBotListener(handler_classes=[], client=MagicMock())
        listener.handlers = [handler_1, handler_2]

        event = MagicMock(event='follow')
        listener.on_event(event)

        handler_1.on_event.assert_called_once_with(event)
        handler_2.on_event.assert_called_once_with(event)

    def test_not_call_handlers_on_unknown_event(self):
        handler = MagicMock(on_event=MagicMock())
        listener = ResponseBotListener(handler_classes=[], client=MagicMock())
        listener.handlers = [handler]

        event = MagicMock(event='unknown')
        listener.on_event(event)

        handler.on_event.assert_not_called()
