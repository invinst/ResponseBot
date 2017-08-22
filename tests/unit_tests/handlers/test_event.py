from unittest.case import TestCase

from responsebot.common.constants import TWITTER_NON_TWEET_EVENTS
from responsebot.handlers.event import BaseEventHandler

try:
    from mock import MagicMock, patch
except ImportError:
    from unittest.mock import MagicMock, patch


class BaseEventHandlerTestCase(TestCase):
    def setUp(self):
        self.handler = BaseEventHandler(client=MagicMock())
        for attr in dir(BaseEventHandler):
            if attr.startswith('on_'):
                setattr(self.handler, attr, MagicMock())

    def test_handle(self):
        event = MagicMock()
        for event_type in TWITTER_NON_TWEET_EVENTS:
            event.event = event_type
            self.handler.handle(event)
            getattr(self.handler, 'on_{event}'.format(event=event_type)).assert_called_once_with(event)
