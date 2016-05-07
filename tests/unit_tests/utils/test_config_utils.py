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
            'consumer_key': 'consumer_key',
            'consumer_secret': 'consumer_secret',
            'token_key': 'token_key',
            'token_secret': 'token_secret',
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
            'consumer_key': 'consumer_key',
            'consumer_secret': 'consumer_secret',
            'token_key': 'token_key',
            'token_secret': 'token_secret',
        }

        config = ResponseBotConfig(**params)

        for config_key in ResponseBotConfig.REQUIRED_CONFIGS:
            self.assertEqual(config.get(config_key), config_key)
