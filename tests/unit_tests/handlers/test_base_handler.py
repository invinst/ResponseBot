from unittest.case import TestCase

try:
    from mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock

from pytest import raises

from responsebot.handlers.base import BaseTweetHandler


class BaseTweetHandlerTestCase(TestCase):
    def test_cannot_instantiate_base_handler(self):
        with raises(NotImplementedError):
            BaseTweetHandler(MagicMock()).on_tweet(tweet=MagicMock())
