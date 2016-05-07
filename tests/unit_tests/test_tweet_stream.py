from unittest.case import TestCase

from tweepy.error import TweepError

from responsebot.common.exceptions import APIError
from responsebot.responsebot_stream import ResponseBotStream

try:
    from mock import patch, MagicMock
except ImportError:
    from unittest.mock import patch, MagicMock


class TweetStreamTestCase(TestCase):
    @patch('responsebot.responsebot_stream.tweepy.Stream.filter', side_effect=TweepError(reason='some mild error'))
    def test_retry_on_non_critical_error(self, mock_stream):
        stream = ResponseBotStream(client=MagicMock(client=MagicMock()), listener=MagicMock())
        stream.start(retry_limit=1)

        self.assertEqual(mock_stream.call_count, 2)

    def test_terminate_on_critical_error(self):
        exception = TweepError(reason='Stream object already connected!')
        with patch('responsebot.responsebot_stream.tweepy.Stream.filter', side_effect=exception) as mock_stream:
            stream = ResponseBotStream(client=MagicMock(client=MagicMock()), listener=MagicMock())

            self.assertRaises(APIError, stream.start)
            self.assertEqual(mock_stream.call_count, 1)

    def test_filter_using_merged_filter(self):
        merged_filter = MagicMock(track=['track'], follow=['follow'])
        stream = ResponseBotStream(client=MagicMock(client=MagicMock()), listener=MagicMock(
                get_merged_filter=MagicMock(return_value=merged_filter)))

        with patch('responsebot.responsebot_stream.tweepy.Stream.filter') as mock_filter_call:
            stream.start(retry_limit=0)

            mock_filter_call.assert_called_once_with(track=merged_filter.track, follow=merged_filter.follow)
