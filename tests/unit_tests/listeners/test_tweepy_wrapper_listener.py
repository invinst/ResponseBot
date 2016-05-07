from unittest.case import TestCase

from responsebot.listeners.tweepy_wrapper_listener import TweepyWrapperListener

try:
    from mock import MagicMock, patch
except ImportError:
    from unittest.mock import MagicMock, patch


class TweepyWrapperListenerTestCase(TestCase):
    def test_call_generic_listener_on_tweet(self):
        generic_listener = MagicMock(on_tweet=MagicMock())
        status = MagicMock(_json={'some key': 'some value'})

        tweet_obj = 'tweet_obj'
        with patch('responsebot.listeners.tweepy_wrapper_listener.Tweet', return_value=tweet_obj) as mock_tweet_obj:
            TweepyWrapperListener(listener=generic_listener).on_status(status)

            mock_tweet_obj.assert_called_once_with(status._json)
            generic_listener.on_tweet.assert_called_once_with(tweet_obj)
