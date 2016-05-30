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

from responsebot.common.exceptions import UserHandlerError
from responsebot.handlers.base import BaseTweetHandler
from responsebot.handlers.event import BaseEventHandler

try:
    from mock import MagicMock, patch
except ImportError:
    from unittest.mock import MagicMock, patch


class Handler(BaseTweetHandler):
    class ValidEventHandler(BaseEventHandler):
        pass

    def __init__(self, *args, **kwargs):
        self.event_handler_class = self.ValidEventHandler
        super(Handler, self).__init__(*args, **kwargs)


class HandlerWithInvalidEventHandler(BaseTweetHandler):
    class InvalidEventHandler(object):
        pass

    def __init__(self, *args, **kwargs):
        self.event_handler_class = self.InvalidEventHandler
        super(HandlerWithInvalidEventHandler, self).__init__(*args, **kwargs)


class HandlerWithErrorneousEventHandler(BaseTweetHandler):
    class ErrorneousEventHandler(BaseEventHandler):
        def __init__(self, client):
            raise Exception

    def  __init__(self, *args, **kwargs):
        self.event_handler_class = self.ErrorneousEventHandler
        super(HandlerWithErrorneousEventHandler, self).__init__(*args, **kwargs)


class BaseTweetHandlerTestCase(TestCase):
    def test_register_event_handler_on_user_stream(self):
        client = MagicMock(config={'user_stream': True})

        handler = Handler(client)

        self.assertTrue(isinstance(handler.event_handler, Handler.ValidEventHandler))

    def test_not_register_event_handler_on_public_stream(self):
        client = MagicMock(config={'user_stream': False})

        handler = Handler(client)

        self.assertIsNone(handler.event_handler)

    def test_only_register_valid_event_handler(self):
        client = MagicMock(config={'user_stream': True})

        handler = HandlerWithInvalidEventHandler(client)

        self.assertIsNone(handler.event_handler)

    def test_raise_user_handler_error_on_event_handler_init_error(self):
        client = MagicMock(config={'user_stream': True})

        self.assertRaises(UserHandlerError, HandlerWithErrorneousEventHandler, client=client)

    def test_call_event_handler_handle(self):
        client = MagicMock()
        handler = Handler(client)
        handler.event_handler=MagicMock()
        event = MagicMock()

        handler.on_event(event)

        handler.event_handler.handle.assert_called_once_with(event)
