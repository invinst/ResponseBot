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
