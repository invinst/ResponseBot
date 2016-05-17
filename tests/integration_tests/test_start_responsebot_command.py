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

from click.testing import CliRunner

from responsebot import start_responsebot

try:
    from mock import patch
except ImportError:
    from unittest.mock import patch


class StartResponseBotCommandTestCase(TestCase):
    def test_call_command(self):
        with patch('responsebot.start_responsebot.ResponseBot.__init__') as mock_responsebot:
            CliRunner().invoke(cli=start_responsebot.main)

            self.assertTrue(mock_responsebot.called)

    def test_call_command_with_handlers_module_option(self):
        handlers_package = 'handlers_package'
        consumer_key = 'ck'
        consumer_secret = 'cs'
        token_key = 'tk'
        token_secret = 'ts'

        with patch('responsebot.start_responsebot.ResponseBot.__init__') as mock_responsebot:
            CliRunner().invoke(cli=start_responsebot.main, args=[
                '--handlers-package', handlers_package,
                '--auth', consumer_key, consumer_secret, token_key, token_secret,
            ])

            mock_responsebot.assert_called_once_with(auth=(consumer_key, consumer_secret, token_key, token_secret),
                                                     handlers_package=handlers_package, user_stream=False)
