from unittest.case import TestCase

from examples.handlers.save_tweet_handler import SaveTweetHandler
from responsebot.models import Tweet

try:
    from mock import MagicMock, patch, call
except ImportError:
    from unittest.mock import MagicMock, patch, call

from responsebot.responsebot_client import ResponseBotClient


class SaveTweetHandlerTestCase(TestCase):
    def test_save_incoming_tweets(self):
        tweet = Tweet({'text': '@bot mornin', 'user': {'screen_name': 'some_bloke'}})
        client = ResponseBotClient(client=MagicMock(me=MagicMock(return_value=MagicMock(_json={'id': 123}))))
        mock_cursor = MagicMock()

        with patch('sqlite3.connect', return_value=MagicMock(cursor=MagicMock(return_value=mock_cursor))):
            handler = SaveTweetHandler(client)

            handler.on_tweet(tweet)

            mock_cursor.execute.assert_has_calls([
                call("CREATE TABLE IF NOT EXISTS tweets (tweet text, username text)"),
                call("INSERT INTO tweets VALUES ('@bot mornin', 'some_bloke')"),
            ])
