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

from dateutil.parser import parse

from responsebot.models import List, User


class ListModelTestCase(TestCase):
    def test_parse_list(self):
        created_at = 'Mon Apr 25 08:25:58 +0000 2016'
        raw = {
            'some_key': 'some value',
            'created_at': created_at,
            'user': {
                'screen_name': 'some_one'
            }
        }

        expected_created_at = parse(created_at)

        list = List(raw)

        self.assertEqual(list.some_key, 'some value')
        self.assertEqual(list.created_at, expected_created_at)

        self.assertTrue(isinstance(list.user, User))
        self.assertEqual(list.user.screen_name, 'some_one')
