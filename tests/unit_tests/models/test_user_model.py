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

from responsebot.models import User, Tweet


class UserModelTestCase(TestCase):
    def test_create_from_raw_data(self):
        created_at = 'Mon Apr 25 08:25:58 +0000 2016'
        raw = {
            'some_key': 'some value',
            'created_at': created_at,
            'status': {
                'created_at': created_at
            },
            'following': True
        }

        expected_created_at = parse(created_at)

        user = User(raw)

        self.assertEqual(user.some_key, 'some value')
        self.assertEqual(user.created_at, expected_created_at)

        self.assertTrue(isinstance(user.tweet, Tweet))
        self.assertEqual(user.tweet.created_at, expected_created_at)

        self.assertEqual(user.following, True)
