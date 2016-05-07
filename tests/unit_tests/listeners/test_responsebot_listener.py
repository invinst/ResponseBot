from unittest.case import TestCase

from responsebot.common.exceptions import UserHandlerError
from responsebot.listeners.responsebot_listener import ResponseBotListener

try:
    from mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock


class ResponseBotListenerTestCase(TestCase):
    def test_register_handlers(self):
        handler_class_1 = MagicMock(return_value='handler 1')
        handler_class_2 = MagicMock(return_value='handler 2')

        listener = ResponseBotListener(handler_classes=[handler_class_1, handler_class_2], client=None)

        self.assertEqual(listener.handlers, ['handler 1', 'handler 2'])

    def test_call_handlers_on_tweet(self):
        handler_1 = MagicMock(on_tweet=MagicMock())
        handler_2 = MagicMock(on_tweet=MagicMock())
        listener = ResponseBotListener(handler_classes=[], client=None)
        listener.handlers = [handler_1, handler_2]

        tweet = MagicMock(text='tweet')
        listener.on_tweet(tweet)

        handler_1.on_tweet.assert_called_once_with(tweet)
        handler_2.on_tweet.assert_called_once_with(tweet)

    def test_raise_user_handler_exception(self):
        handler_class = MagicMock(side_effect=Exception('some error'))

        self.assertRaises(UserHandlerError, ResponseBotListener, handler_classes=[handler_class], client=None)

    def test_raise_user_handler_exception_on_tweet(self):
        handler_class = MagicMock()
        handler_class().on_tweet = MagicMock(side_effect=Exception('some error unknown'))
        tweet = MagicMock(text='tweet')

        listener = ResponseBotListener(handler_classes=[handler_class], client=None)

        self.assertRaises(UserHandlerError, listener.on_tweet, tweet=tweet)

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
