# Copyright 2016 Invisible Institute
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
        stream = ResponseBotStream(client=MagicMock(client=MagicMock()), listener=MagicMock(), user_stream=False)
        stream.start(retry_limit=1)

        self.assertEqual(mock_stream.call_count, 2)

    def test_terminate_on_critical_error(self):
        exception = TweepError(reason='Stream object already connected!')
        with patch('responsebot.responsebot_stream.tweepy.Stream.filter', side_effect=exception) as mock_stream:
            stream = ResponseBotStream(client=MagicMock(client=MagicMock()), listener=MagicMock(), user_stream=False)

            self.assertRaises(APIError, stream.start)
            self.assertEqual(mock_stream.call_count, 1)

    def test_filter_using_merged_filter(self):
        merged_filter = MagicMock(track=['track'], follow=['follow'])
        stream = ResponseBotStream(client=MagicMock(client=MagicMock()), listener=MagicMock(
                get_merged_filter=MagicMock(return_value=merged_filter)), user_stream=False)

        with patch('responsebot.responsebot_stream.tweepy.Stream.filter') as mock_filter_call:
            stream.start(retry_limit=0)

            mock_filter_call.assert_called_once_with(track=merged_filter.track, follow=merged_filter.follow)

    def test_use_user_stream(self):
        merged_filter = MagicMock(track=['track'])
        stream = ResponseBotStream(client=MagicMock(client=MagicMock()), listener=MagicMock(
                get_merged_filter=MagicMock(return_value=merged_filter)), user_stream=True)

        with patch('responsebot.responsebot_stream.tweepy.Stream.userstream') as mock_user_stream_call:
            stream.start(retry_limit=0)

            mock_user_stream_call.assert_called_once_with(track=merged_filter.track)
