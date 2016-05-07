from unittest.case import TestCase

from tweepy.error import TweepError

from responsebot.common.exceptions import AuthenticationError
from responsebot.responsebot_client import ResponseBotClient

try:
    from mock import patch, MagicMock
except ImportError:
    from unittest.mock import patch, MagicMock

from responsebot.utils import auth_utils


class AuthUtilsTestCase(TestCase):
    def test_failed_auth(self):
        with patch('responsebot.utils.auth_utils.tweepy.API.verify_credentials',
                   side_effect=TweepError(reason=[{'message': 'some message'}])):
            self.assertRaises(
                AuthenticationError,
                auth_utils.auth,
                consumer_key='ck', consumer_secret='cs', token_key='tk', token_secret='ts'
            )

    @patch('responsebot.utils.auth_utils.tweepy.API.verify_credentials')
    @patch('responsebot.utils.auth_utils.tweepy.API.me', return_value=MagicMock(screen_name='me'))
    def test_successful_auth(self, mock_me, mock_verify):
        try:
            client = auth_utils.auth(consumer_key='ck', consumer_secret='cs', token_key='tk', token_secret='ts')
        except AuthenticationError:
            self.fail('Expected no authentication error')
        else:
            self.assertIsInstance(client, ResponseBotClient)
