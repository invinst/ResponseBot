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

        with patch('responsebot.start_responsebot.ResponseBot.__init__') as mock_responsebot:
            CliRunner().invoke(cli=start_responsebot.main, args=['--handlers-package', handlers_package])

            mock_responsebot.assert_called_once_with(handlers_package=handlers_package)
