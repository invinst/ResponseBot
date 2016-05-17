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

from responsebot.common.exceptions import MissingConfigError, APIQuotaError, AuthenticationError, APIError, \
    UserHandlerError

try:
    from mock import patch, MagicMock
except ImportError:
    from unittest.mock import patch, MagicMock

from responsebot.responsebot import ResponseBot


class ResponseBotTestCase(TestCase):
    def test_call_necessary_utils(self):
        handler_classes = [MagicMock]
        client = MagicMock()
        listener = MagicMock()

        with patch('responsebot.utils.handler_utils.discover_handler_classes', return_value=handler_classes) \
                as mock_discover, \
                patch('responsebot.utils.auth_utils.auth', return_value=client) as mock_auth, \
                patch('responsebot.responsebot.ResponseBotListener', return_value=listener) as mock_listener, \
                patch('responsebot.responsebot.ResponseBotStream') as mock_stream:
            ResponseBot(
                handlers_package='some_package',
                auth=('ck', 'cs', 'tk', 'ts'),
            ).start()

            self.assertTrue(mock_auth.called)
            self.assertTrue(mock_discover.called)
            mock_listener.assert_called_once_with(client=client, handler_classes=handler_classes)
            mock_stream.assert_called_once_with(client=client, listener=listener, user_stream=False)
            mock_stream().start.assert_called_once_with()

    @patch('logging.error')
    def test_log_missing_config_exception(self, mock_log):
        exception = MissingConfigError('message')

        with patch('responsebot.responsebot.ResponseBotConfig', side_effect=exception):
            self.assertRaises(SystemExit, ResponseBot)
            mock_log.assert_called_once_with('message')

    @patch('logging.warning')
    def test_log_no_handler_classes_warning(self, mock_log):
        with patch('responsebot.responsebot.ResponseBotConfig'),\
                patch('responsebot.utils.handler_utils.discover_handler_classes', return_value=[]),\
                patch('responsebot.utils.auth_utils.auth'),\
                patch('responsebot.responsebot.ResponseBotStream'):
            ResponseBot().start()
            mock_log.assert_called_once_with('No handler found. Did you forget to extend BaseTweethandler?'
                                             ' Check --handlers-module')

    @patch('logging.error')
    def test_log_import_handler_error(self, mock_log):
        exception = ImportError('message')
        with patch('responsebot.responsebot.ResponseBotConfig'),\
                patch('responsebot.utils.handler_utils.discover_handler_classes', side_effect=exception):
            self.assertRaises(SystemExit, ResponseBot().start)
            mock_log.assert_called_once_with('message')

    @patch('logging.error')
    def test_log_auth_error(self, mock_log):
        for exception in [APIQuotaError('message'), AuthenticationError('message')]:
            mock_log.reset_mock()
            with patch('responsebot.responsebot.ResponseBotConfig'),\
                    patch('responsebot.utils.handler_utils.discover_handler_classes', return_value=[MagicMock]),\
                    patch('responsebot.utils.auth_utils.auth', side_effect=exception):
                self.assertRaises(SystemExit, ResponseBot().start)
                mock_log.assert_called_once_with('message')

    @patch('logging.error')
    def test_log_stream_api_error(self, mock_log):
        exception = APIError('message')
        with patch('responsebot.responsebot.ResponseBotConfig'),\
                patch('responsebot.utils.handler_utils.discover_handler_classes', return_value=[MagicMock]),\
                patch('responsebot.utils.auth_utils.auth'),\
                patch('responsebot.responsebot.ResponseBotListener'),\
                patch('responsebot.responsebot.ResponseBotStream', side_effect=exception):
            self.assertRaises(SystemExit, ResponseBot().start)
            mock_log.assert_called_once_with('message')

    @patch('logging.exception')
    def test_log_user_handler_error(self, mock_log):
        exception = UserHandlerError('message')
        with patch('responsebot.responsebot.ResponseBotConfig'),\
                patch('responsebot.utils.handler_utils.discover_handler_classes', return_value=[MagicMock]),\
                patch('responsebot.utils.auth_utils.auth'),\
                patch('responsebot.responsebot.ResponseBotListener', side_effect=exception),\
                patch('responsebot.responsebot.ResponseBotStream', side_effect=exception):
            self.assertRaises(SystemExit, ResponseBot().start)
            mock_log.assert_called_once_with(exception)
