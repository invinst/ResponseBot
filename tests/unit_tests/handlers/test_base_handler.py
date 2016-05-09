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

try:
    from mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock

from pytest import raises

from responsebot.handlers.base import BaseTweetHandler


class BaseTweetHandlerTestCase(TestCase):
    def test_cannot_instantiate_base_handler(self):
        with raises(NotImplementedError):
            BaseTweetHandler().on_tweet(tweet=MagicMock())
