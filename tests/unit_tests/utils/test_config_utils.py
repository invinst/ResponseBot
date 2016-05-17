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

from responsebot.common.exceptions import MissingConfigError

try:
    from mock import patch
except ImportError:
    from unittest.mock import patch

from responsebot.utils.config_utils import ResponseBotConfig


class ConfigUtilsTestCase(TestCase):
    def test_raise_exception_if_missing_required_config(self):
        self.assertRaises(Exception, ResponseBotConfig)

    def test_validate_config(self):
        params = {
            'handlers_package': 'handlers_package',
            'auth': ('consumer_key', 'consumer_secret', 'token_key', 'token_secret'),
        }
        try:
            ResponseBotConfig(**params)
        except MissingConfigError:
            self.fail('Should not raise missing exception')

    @patch('responsebot.utils.config_utils.SafeConfigParser.has_section', return_value=True)
    @patch('responsebot.utils.config_utils.SafeConfigParser.get', return_value='some_config')
    def test_load_config_from_file(self, mock_1, mock_2):
        config = ResponseBotConfig()

        for config_key in ResponseBotConfig.REQUIRED_CONFIGS:
            self.assertEqual(config.get(config_key), 'some_config')

    @patch('responsebot.utils.config_utils.SafeConfigParser.has_section', return_value=True)
    @patch('responsebot.utils.config_utils.SafeConfigParser.get', return_value='some_config')
    def test_load_config_from_terminal(self, mock_1, mock_2):
        params = {
            'handlers_package': 'handlers_package',
            'auth': ('consumer_key', 'consumer_secret', 'token_key', 'token_secret'),
        }

        config = ResponseBotConfig(**params)

        for config_key in ResponseBotConfig.REQUIRED_CONFIGS:
            self.assertEqual(config.get(config_key), config_key)
